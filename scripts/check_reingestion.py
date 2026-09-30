#!/usr/bin/env python3
import json
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from romanwiki.runtime import ROOT
from romanwiki.sources import checksum
from romanwiki.ingest import ingest,load_state

def snapshot():
    state=load_state()
    return {'files':{str(p.relative_to(ROOT)):checksum(p) for p in (ROOT/'vault').rglob('*') if p.is_file() and '.obsidian' not in str(p)},
            'note_paths':{k:v['path'] for k,v in state['notes'].items()}}
if __name__=='__main__':
    before=snapshot();runs=ingest(ROOT/'vault/raw');after=snapshot()
    result={'unchanged':before==after,'before':before,'after':after,'runs':runs}
    (ROOT/'results/reingestion.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'unchanged':before==after,'note_count':len(after['note_paths'])},indent=2));sys.exit(before!=after)
