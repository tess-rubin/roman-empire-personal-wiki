#!/usr/bin/env python3
"""Explicit connected setup only; never invoked by the CLI or offline runner."""
import hashlib
import json
import urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
for key,info in json.loads((ROOT/'config/sources.json').read_text()).items():
    path=ROOT/'vault/raw'/info['file']
    if path.exists():
        data=path.read_bytes()
    else:
        with urllib.request.urlopen(info['url'],timeout=60) as r:data=r.read()
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_bytes(data)
    actual=hashlib.sha256(data).hexdigest()
    if actual!=info['sha256']:
        raise SystemExit(f'{key}: upstream bytes differ from recorded SHA-256. Original preserved; inspect edition before updating the profile.')
    print(key,actual)
