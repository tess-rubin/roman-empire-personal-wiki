#!/usr/bin/env python3
"""Explicit connected setup only; never invoked by the CLI or offline runner."""
import hashlib
import json
import ssl
import urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
# Use the system trust store when standalone macOS Python lacks bundled roots.
SYSTEM_CA=Path('/etc/ssl/cert.pem')
TLS=ssl.create_default_context(cafile=str(SYSTEM_CA) if SYSTEM_CA.exists() else None)
for key,info in json.loads((ROOT/'config/sources.json').read_text()).items():
    path=ROOT/'vault/raw'/info['file']
    if path.exists():
        data=path.read_bytes()
    else:
        with urllib.request.urlopen(info['url'],timeout=60,context=TLS) as r:data=r.read()
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_bytes(data)
    actual=hashlib.sha256(data).hexdigest()
    if actual!=info['sha256']:
        raise SystemExit(f'{key}: upstream bytes differ from recorded SHA-256. Original preserved; inspect edition before updating the profile.')
    print(key,actual)
