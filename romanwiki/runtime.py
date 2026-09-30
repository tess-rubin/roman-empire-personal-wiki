"""Small loopback-only Ollama adapter with auditable measurements."""
import contextlib
import fcntl
import json
import os
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path
import psutil

MODEL='gemma4:e2b-it-qat'
URL='http://127.0.0.1:11435'
OPTIONS={'num_ctx':4096,'num_predict':850,'temperature':0.1,'seed':42}
ROOT=Path(__file__).resolve().parents[1]

class WikiError(Exception):
    pass


def snapshot():
    processes=[]
    measurement_errors=[]
    try: observed=list(psutil.process_iter(['pid','name','memory_info']))
    except (PermissionError,psutil.AccessDenied) as e:
        observed=[];measurement_errors.append('Process memory unavailable: '+str(e))
    for p in observed:
        try:
            if any(n in (p.info['name'] or '').lower() for n in ['ollama','llama-server']):
                processes.append({'pid':p.pid,'name':p.info['name'],'rss':p.info['memory_info'].rss})
        except (psutil.NoSuchProcess,psutil.AccessDenied): pass
    def measure(name,call):
        try:return call()
        except (PermissionError,psutil.AccessDenied,OSError) as e:
            measurement_errors.append(name+' unavailable: '+str(e));return None
    return {'time':time.time(),'python_rss':measure('python RSS',lambda:psutil.Process().memory_info().rss),
            'system':measure('system memory',lambda:psutil.virtual_memory()._asdict()),'swap':measure('swap',lambda:psutil.swap_memory()._asdict()),
            'ollama_processes':processes,'measurement_errors':measurement_errors}


def http(route,payload=None):
    # Disable environment proxy configuration; no host is accepted from user input.
    opener=urllib.request.build_opener(urllib.request.ProxyHandler({}))
    req=urllib.request.Request(URL+route,data=None if payload is None else json.dumps(payload).encode(),
                               headers={'Content-Type':'application/json'})
    try:
        with opener.open(req,timeout=240) as response: return json.load(response)
    except urllib.error.HTTPError as e:
        detail=e.read().decode(errors='replace')
        raise WikiError(f'Runtime HTTP {e.code}: {detail}. Check selected weights with scripts/start_ollama.sh and ollama list.') from e
    except (urllib.error.URLError,TimeoutError,OSError) as e:
        raise WikiError(f'Local Gemma unavailable at {URL}. Run scripts/start_ollama.sh; download weights explicitly during setup. No cloud fallback. ({e})') from e
    except ValueError as e: raise WikiError('Malformed Ollama HTTP JSON response.') from e


def identity():
    tags=http('/api/tags').get('models',[])
    match=next((m for m in tags if m.get('name')==MODEL),None)
    if not match:raise WikiError(f'Missing weights: while connected run OLLAMA_HOST=127.0.0.1:11435 ollama pull {MODEL}. Normal commands never download.')
    return {'model':match,'runtime':http('/api/version'),'show':http('/api/show',{'model':MODEL})}


@contextlib.contextmanager
def lock(name):
    (ROOT/'data').mkdir(exist_ok=True)
    with (ROOT/'data'/f'{name}.lock').open('w') as handle:
        fcntl.flock(handle,fcntl.LOCK_EX)
        yield


def generate(messages,structured=False):
    with lock('runtime'):
        model=identity()
        samples=[snapshot()]; stop=threading.Event()
        def sample():
            while not stop.wait(0.5): samples.append(snapshot())
        thread=threading.Thread(target=sample,daemon=True);thread.start()
        start=time.perf_counter()
        payload={'model':MODEL,'messages':messages,'stream':False,'options':OPTIONS,'keep_alive':'10m','think':False}
        if structured:payload['format']=ANSWER_SCHEMA
        try: response=http('/api/chat',payload)
        finally:
            stop.set();thread.join();samples.append(snapshot())
        if not response.get('done') or response.get('done_reason')=='length':
            raise WikiError('Incomplete/truncated model response; reduce evidence or raise output budget within context.')
        return {'identity':model,'settings':OPTIONS,'request':payload,'response':response,
                'wall_seconds':time.perf_counter()-start,'memory_samples':samples,'allocation':http('/api/ps')}


ANSWER_SCHEMA={
 "type":"object","required":["status","explanation","claims"],"additionalProperties":False,
 "properties":{
  "status":{"type":"string","enum":["answered","insufficient"]},
  "explanation":{"type":"string"},
  "claims":{"type":"array","maxItems":4,"items":{
   "type":"object","required":["text","citations"],"additionalProperties":False,
   "properties":{"text":{"type":"string"},"citations":{"type":"array","minItems":1,"maxItems":3,"items":{
    "type":"object","required":["id","path","quote"],"additionalProperties":False,
    "properties":{"id":{"type":"string"},"path":{"type":"string"},"quote":{"type":"string"}}}}}}}}}
