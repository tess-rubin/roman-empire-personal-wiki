"""Edition-specific extraction. Only source passages enter the evidence index."""
import hashlib
import re
from bs4 import BeautifulSoup


def checksum(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def clean(text):
    return re.sub(r'\s+', ' ', text.replace('\xad', '').replace('\u2060', '')).strip()


def extract(source, path):
    soup = BeautifulSoup(path.read_bytes(), 'html.parser')
    records = []
    if source == 'augustus':
        for cell in soup.select('td.English'):
            anchor = cell.select_one('a.chapter')
            sec = anchor.get('name')
            for junk in cell.select('a.ref, .pagenum, a.chapter'):
                junk.decompose()
            records.append((sec, sec, clean(cell.get_text())))
    elif source == 'tacitus':
        # MIT labels lines, not chapters. These verified chapter boundaries are
        # stable for this preserved edition. Chapter 44 includes its second paragraph.
        boundaries = [(38,650,681),(39,681,694),(40,694,708),(41,708,723),
                      (42,723,739),(43,739,765),(44,765,795)]
        html = path.read_text()
        for sec, start, end in boundaries:
            a = re.search(r'<A NAME="'+str(start)+r'">', html).start()
            b = re.search(r'<A NAME="'+str(end)+r'">', html).start()
            records.append((str(sec),str(start),clean(BeautifulSoup(html[a:b], 'html.parser').get_text())))
    elif source == 'pliny':
        allowed = {'XLII','XLIII','XLIV','XLV','XLVI','XLVII'}
        for heading in soup.find_all('h2'):
            title = clean(heading.get_text())
            sec = title.split(' ')[0]
            if sec not in allowed or not ('TRAJAN' in title):
                continue
            anchor = heading.find_previous('a',id=True)['id']
            parts=[]
            for sibling in heading.next_siblings:
                if getattr(sibling,'name',None)=='h2': break
                if getattr(sibling,'name',None)=='p':
                    for footnote in sibling.select('a.pginternal'): footnote.decompose()
                    parts.append(sibling.get_text())
            records.append((sec,anchor,clean(' '.join(parts))))
    else:
        raise ValueError('Unsupported source: add an explicit source profile, never index arbitrary prompts or notes.')
    if not records or any(not text for _,_,text in records):
        raise ValueError('Extraction failed; original edition may have changed.')
    return records


def passages(source, path, expected):
    records = extract(source,path)
    if [r[0] for r in records] != expected:
        raise ValueError('Extracted sections differ from the source profile.')
    out=[]
    for section,anchor,text in records:
        # Keep short sections intact; split long sections at sentence boundaries.
        sentences = re.split(r'(?<=[.!?])\s+',text)
        groups=[]; current=[]; count=0
        for sentence in sentences:
            n=len(sentence.split())
            if current and count+n>250:
                groups.append(' '.join(current)); current=[];count=0
            current.append(sentence);count+=n
        if current:groups.append(' '.join(current))
        for i,chunk in enumerate(groups,1):
            out.append({'id':f'{source}:{section}:{i}','source':source,'section':f'{source}:{section}',
                        'path':f'vault/raw/{path.name}#{anchor}','text':chunk,'attribution':attribution(source,section)})
    return out


def attribution(source,section):
    if source=="pliny":
        return "Trajan replying to Pliny" if section in {"XLIII","XLV","XLVII"} else "Pliny writing to Trajan"
    if source=="augustus":return "Appended Res Gestae summary (third person)" if section.startswith("S") else "Augustus’s self-account"
    return "Tacitus, Annals XV (Church–Brodribb translation)"
