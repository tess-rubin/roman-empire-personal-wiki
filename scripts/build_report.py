#!/usr/bin/env python3
"""Render saved evaluation records; never substitute new text for model output."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
EVAL=ROOT/'results/offline-20260929T215714'
RUN=ROOT/'results/offline-20260929T215623'
OUT=ROOT/'results/evidence-cards';OUT.mkdir(exist_ok=True)
reviews={
'augustus':['Pass. Res Gestae 34 appears in retrieval.','Claim 1 paraphrases Augustus’s claim to transfer control; claim 2 lists honors expressly stated in the same passage; claim 3 correctly preserves precedence in rank versus no greater magistrates’ power. All are attributed to Augustus.','The honors are supported but more background than the question needs. This is a self-account, not independent confirmation of political reality.'],
'nero':['Pass for grounded content and required relief measures. Annals 15.39 appears in retrieval.','Claim 1 and its quotation cover opened spaces/buildings and temporary shelters; claim 2 covers imported food and cheaper corn. Claims 3–4 on colonnades and debris are supported by 15.43, though less directly relevant.','The model did not say “According to Tacitus” in the prose. The citation IDs and evidence attribution identify Tacitus; read all four as his account. Explicit prose attribution remains an improvement. No claim here repeats the singing rumour as fact.'],
'pliny':['Pass. Both XLVI and XLVII appear in retrieval.','Claim 1 correctly connects prior failure with Pliny’s request for a waterworks specialist. Claim 2 correctly assigns the investigation of wasted expenditure and concern over diversion to Trajan. Both quotes support the claims.','The answer does not name a guilty person or establish that diversion occurred. It omits Trajan’s additional instruction to report results and ensure water provision, but covers the fixed evaluation target.'],
'unsupported':['Pass. The selected passages do not provide an exact death toll.','The actual model response explicitly states insufficient evidence and supplies no invented figure or citation. Relevant fire passages were retrieved; the system did not merely avoid generation because the index was empty.','This conclusion concerns the selected corpus; it is not a claim about every surviving ancient source.']}
for key,review in reviews.items():
    r=json.loads((EVAL/(key+'.json')).read_text());run=r['run']
    text=f'# Evidence card — {key.title()}\n\n{r["question"]}\n\n'
    text+=f'Execution: local Gemma during the verified offline run. Model `{run["identity"]["model"]["name"]}`, digest `{run["identity"]["model"]["digest"]}`, Ollama `{run["identity"]["runtime"]["version"]}`.\n\n'
    text+=f'Settings: `{json.dumps(run["settings"])}`. Model-call wall time: **{run["wall_seconds"]:.2f} s**.\n\n'
    text+=f'[Exact JSON record](../{EVAL.name}/{key}.json) · [Offline proof](../{RUN.name}/runner-summary.json)\n\n## Independent claim review\n\n'+'\n\n'.join(review)+'\n\n## Actual displayed model response\n\n'
    text+='```text\n'+r['display']+'\n```\n\n## Retrieved original passages\n\n'
    for p in r['retrieved']:
        text+=f'### {p["id"]}\n\nAttribution: {p.get("attribution",p["source"])}. Location: `{p["path"]}`. BM25: {p["score"]:.4f}.\n\n> '+p['text']+'\n\n'
    (OUT/(key+'.md')).write_text(text)
records=[]
for p in sorted((ROOT/'results/runs').glob('20260929T215*.json')):
    r=json.loads(p.read_text())
    if 'run' in r:records.append((p,r,r['run']))
measurements=[]
for p,r,run in records:
    samples=run['memory_samples']
    measurements.append({'record':str(p.relative_to(ROOT)),'mode':r['mode'],'seconds':run['wall_seconds'],
      'python_peak_rss':max(s['python_rss'] for s in samples),
      'ollama_peak_process_rss_sum':max(sum(proc['rss'] for proc in s['ollama_processes']) for s in samples),
      'minimum_available':min(s['system']['available'] for s in samples),
      'maximum_swap_used':max(s['swap']['used'] for s in samples),
      'allocation':run['allocation'],'load_seconds':run['response'].get('load_duration',0)/1e9})
(ROOT/'results/measurements.json').write_text(json.dumps(measurements,indent=2)+'\n')
gib=lambda n:n/1024**3
mib=lambda n:n/1024**2
text='# Observed measurements\n\nFinal verified offline run; these are actual observations, not model-size estimates. Samples every 0.5 seconds can miss brief peaks. Process RSS is not unique physical allocation; shared pages can overlap. No RSS/GPU/available-memory totals are added together.\n\n'
text+='| Call | Wall seconds | Python peak MiB | Ollama process RSS sum peak GiB | Minimum available GiB | Maximum swap GiB |\n|---|---:|---:|---:|---:|---:|\n'
for m in measurements:
 text+=f'| [{m["mode"]}](../{m["record"]}) | {m["seconds"]:.2f} | {mib(m["python_peak_rss"]):.1f} | {gib(m["ollama_peak_process_rss_sum"]):.2f} | {gib(m["minimum_available"]):.2f} | {gib(m["maximum_swap_used"]):.2f} |\n'
text+='\nThe first two calls are the same Augustus question: cold after runtime restart, then warm. The first includes model loading; OS disk caches were not flushed. Final Pliny re-ingestion/redrafting took 15.68 seconds end to end. The first-ever Pliny ingestion occurred in the earlier network-interrupted run (68.47 seconds; see results/runs/20260929T170515-40ab429e.json).\n\n'
alloc=measurements[0]['allocation']['models'][0]
text+=f'Ollama `/api/ps` reported `size={alloc["size"]}` and `size_vram={alloc["size_vram"]}` bytes with context length {alloc["context_length"]}. Both describe the same reported model allocation; they are not two physical-RAM pools. This runtime-reported figure is not the downloaded model size or a measurement of total physical memory consumed. The full API response is preserved.\n\n'
text+='[Machine-readable measurements](measurements.json). Initial connected samples omitted the separate llama-server process; they must not be cited as total inference RSS. The final run includes it. All-app workload changed between runs, so these are not controlled speed benchmarks.\n'
(ROOT/'results/measurements.md').write_text(text)
print(text)
