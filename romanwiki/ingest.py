"""Transactional source indexing and review-first note generation."""
import json
import shutil
import time
from pathlib import Path
from urllib.parse import quote
from .runtime import ROOT,WikiError,generate,lock,snapshot
from .sources import checksum,passages
from .store import index
from .harness import save,validate


def load_state():
    p=ROOT/'data/mappings.json'
    return json.loads(p.read_text()) if p.exists() else {'sources':{},'notes':{}}


def write_state(state):
    p=ROOT/'data/mappings.json';p.parent.mkdir(exist_ok=True)
    tmp=p.with_suffix('.tmp');tmp.write_text(json.dumps(state,indent=2)+'\n');tmp.replace(p)


def catalog():return json.loads((ROOT/'config/sources.json').read_text())


def note_markdown(spec,answer,rows,digest):
    title=spec['title'];source=spec['source'];info=catalog()[source]
    refs={p['path'] for p in rows}
    text=f'---\nsource_id: {source}\nsource_sha256: {digest}\nnote_key: {spec["key"]}\nreview_status: staged\n---\n\n# {title}\n\n## Summary\n\n'
    text+=answer['claims'][0]['text']+'\n\n## Supported details\n\n'
    for claim in answer['claims']:
        text+='- '+claim['text']+' '+ ' '.join(f'[{c["id"]}]' for c in claim['citations'])+'\n'
    text+='\n## Local sources\n\n'+info['author']+'; '+info['translation']+'.\n\n'
    text+=f'[[raw/{info["file"]}|Open the unchanged original HTML]] (open externally if prompted).\n\n'
    for path in sorted(refs):
        text+=f'- [{path}](../../{quote(path.removeprefix('vault/'),safe="/#:")})\n'
    text+='\n## Related notes\n\n'
    reasons={'Augustan Authority':'Connects public activity with Augustus’s account of his standing.',
             'Augustan Diplomacy':'Explores Augustus’s presentation of relations with foreign rulers.',
             'Imperial Public Works':'Compares urban construction and imperial spending.',
             'Great Fire of Rome':'Provides the disaster context for rebuilding.',
             'Rebuilding Rome':'Follows the response from relief to urban construction.',
             'Nicomedia Aqueduct':'Gives a concrete case of provincial construction and oversight.',
             'Provincial Oversight':'Places the aqueduct correspondence alongside administrative decisions.'}
    for related in spec['related']:text+=f'- [[{related}]] — {reasons.get(related, 'Connects this topic with a related source-based note.')}\n'
    return text


def rebuild_index_page(state):
    specs=json.loads((ROOT/'config/notes.json').read_text())
    text='# Roman Empire Personal Wiki\n\nStudy emperors, city life, and government through attributed ancient accounts.\n\n'
    for category in ['Emperors','Cities','Government']:
        text+='## '+category+'\n\n'
        for spec in specs:
            if spec['folder']!=category:continue
            mapping=state['notes'].get(spec['key'])
            if mapping and (ROOT/mapping['path']).exists():
                title=Path(mapping['path']).stem
                text+=f'- [[{title}]] — {catalog()[spec["source"]]["title"]}.\n'
        text+='\n'
    text+='## Source catalog\n\nOriginal HTML files are preserved byte for byte. Only the listed sections enter search.\n\n'
    for key,info in catalog().items():
        text+=f'### {info["title"]}\n\n- [{info["file"]}](raw/{info["file"]}) — {info["author"]}; {info["translation"]}.\n- Indexed scope: {", ".join(info["sections"])}.\n- Source ID: `{key}`. SHA-256: `{info["sha256"]}`.\n- {info["rights"]}\n- [Download source]({info["url"]}).\n\n'
    (ROOT/'vault/index.md').write_text(text)


def ingest(path,redraft=False):
    started=time.perf_counter();before=snapshot()
    path=Path(path)
    if not path.exists():raise WikiError(f'Missing input: {path}. Supply one of the downloaded source HTML files.')
    if path.is_dir():
        return [ingest(p,redraft) for p in sorted(path.glob('*.html'))]
    configs=catalog();digest=checksum(path)
    source=next((s for s,v in configs.items() if v['sha256']==digest),None)
    if source is None:raise WikiError('Unrecognized source checksum. Add/review an explicit config/sources.json profile first; notes and prompts cannot be ingested.')
    with lock('ingest'):
        destination=ROOT/'vault/raw'/configs[source]['file']
        if destination.exists() and checksum(destination)!=digest:raise WikiError('Original collision: refusing to overwrite preserved bytes.')
        if not destination.exists():shutil.copyfile(path,destination)
        rows=passages(source,destination,configs[source]['sections'])
        state=load_state();specs=[s for s in json.loads((ROOT/'config/notes.json').read_text()) if s['source']==source]
        # Source indexing is independent of draft success. Invalid drafts never enter FTS.
        index(source,rows)
        state['sources'][source]={'sha256':digest,'sections':configs[source]['sections'],'passages':len(rows)}
        write_state(state)
        staged=[]
        for spec in specs:
            mapping=state['notes'].setdefault(spec['key'],{'path':f'vault/wiki/{spec["folder"]}/{spec["title"]}.md'})
            reviewed=ROOT/mapping['path'];draft=ROOT/'data/staging'/(spec['key']+'.md')
            if mapping.get('source_sha256')==digest and not redraft and (reviewed.exists() or draft.exists()):continue
            evidence=[r for r in rows if r['section'].split(':')[1] in spec['sections']]
            # A note is generated from its source sections, never the test answer key.
            prompt={'task':f'Draft a short study note titled {spec["title"]}. Return 2–3 concise supported claims. The first claim should summarize the topic. Cite exact excerpts for every claim.','evidence':evidence}
            run=generate([{'role':'system','content':(ROOT/'instructions/research.md').read_text()}, {'role':'user','content':json.dumps(prompt,ensure_ascii=False)}],structured=True)
            record={'mode':'ingest-draft','source':source,'note':spec['key'],'retrieved':evidence,'run':run}
            try:
                answer=json.loads(run['response']['message']['content']);validate(answer,evidence)
                if answer['status']!='answered':raise WikiError('Note generation returned insufficient evidence; review source extraction.')
            except Exception as e:record['error']=str(e);save(record);raise WikiError(f'Invalid draft for {spec["title"]}: {e}') from e
            record['answer']=answer;record_path=save(record)
            draft.parent.mkdir(parents=True,exist_ok=True)
            draft.write_text(note_markdown(spec,answer,evidence,digest))
            mapping.update(source_sha256=digest,staged=str(draft.relative_to(ROOT)),draft_record=record_path)
            staged.append(str(draft.relative_to(ROOT)))
            write_state(state) # completed drafts survive a later failure
        index(source,rows)
        state['sources'][source]={'sha256':digest,'sections':configs[source]['sections'],'passages':len(rows)}
        write_state(state);rebuild_index_page(state)
    result={'mode':'ingest','source':source,'sha256':digest,'staged':staged,'passages':len(rows),
            'wall_seconds':time.perf_counter()-started,'before':before,'after':snapshot()}
    result['record_path']=save(result);return result


def approve(key):
    with lock('ingest'):
        state=load_state();mapping=state['notes'].get(key)
        if not mapping or not mapping.get('staged'):raise WikiError('No staged draft for that note key.')
        draft=ROOT/mapping['staged'];target=ROOT/mapping['path']
        if target.exists():
            backup=ROOT/'data/review-backups'/f'{key}-{time.time_ns()}.md';backup.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(target,backup)
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text(draft.read_text().replace('review_status: staged','review_status: reviewed'))
        mapping['reviewed_sha256']=checksum(target);mapping['reviewed_at']=time.time()
        mapping.pop('staged');draft.unlink();write_state(state);rebuild_index_page(state)
        return str(target.relative_to(ROOT))


def rename(key,title):
    if not re_full_title(title):raise WikiError('Use a short descriptive title with letters, numbers, spaces or hyphens.')
    with lock('ingest'):
        state=load_state();mapping=state['notes'].get(key)
        if not mapping:raise WikiError('Unknown note key.')
        old=ROOT/mapping['path'];new=old.with_name(title+'.md')
        if new.exists():raise WikiError('Title already exists.')
        if mapping.get('staged'):raise WikiError('Review pending draft before renaming.')
        if any(p.stem==title for p in (ROOT/'vault/wiki').rglob('*.md')):raise WikiError('Ambiguous title already exists.')
        text=old.read_text().replace('# '+old.stem+'\n','# '+title+'\n',1)
        new.write_text(text);old.unlink()
        for page in (ROOT/'vault').rglob('*.md'):
            page.write_text(page.read_text().replace('[['+old.stem+']]','[['+title+']]'))
        mapping['path']=str(new.relative_to(ROOT));mapping['reviewed_sha256']=checksum(new)
        # Persistent specifications prevent future redrafts from restoring old names/links.
        specs=json.loads((ROOT/'config/notes.json').read_text())
        for spec in specs:
            if spec['key']==key:spec['title']=title
            spec['related']=[title if n==old.stem else n for n in spec['related']]
        (ROOT/'config/notes.json').write_text(json.dumps(specs,indent=2)+'\n')
        write_state(state)
        for source in state['sources']:
            info=catalog()[source];index(source,passages(source,ROOT/'vault/raw'/info['file'],info['sections']))
        rebuild_index_page(state)
        return f'Renamed to {new.relative_to(ROOT)}; source retrieval paths remain original-source paths. Rerun scripts/evaluate.py.'


def re_full_title(title):
    import re
    return re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9 -]{1,60}',title)
