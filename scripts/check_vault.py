#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from romanwiki.runtime import ROOT
from romanwiki.ingest import load_state
from romanwiki.sources import checksum

def check(require_all=True):
    notes=list((ROOT/'vault/wiki').rglob('*.md'));titles=[p.stem for p in notes];errors=[]
    if require_all and len(notes)!=7:errors.append(f'Expected seven notes; found {len(notes)}')
    if len(titles)!=len(set(titles)):errors.append('Ambiguous duplicate titles')
    for page in notes:
        text=page.read_text()
        if '# '+page.stem+'\n' not in text:errors.append(f'Heading mismatch: {page}')
        for target in re.findall(r'\[\[([^]|]+)(?:\|[^]]+)?\]\]',text):
            if target not in titles and not (ROOT/'vault'/target).is_file():errors.append(f'Missing related note {target} in {page.name}')
        for target in re.findall(r'\]\(([^)]+)\)',text):
            if '://' in target:continue
            p=page.parent/unquote(target.split('#')[0])
            if not p.is_file():errors.append(f'Missing local source: {target}')
    state=load_state()
    for key,info in state['notes'].items():
        if not (ROOT/info['path']).is_file():errors.append('Unreviewed/missing note: '+key)
    return {'notes':len(notes),'titles':titles,'errors':errors}
if __name__=='__main__':
    result=check();print(json.dumps(result,indent=2));sys.exit(bool(result['errors']))
