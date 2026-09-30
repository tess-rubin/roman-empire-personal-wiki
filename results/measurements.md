# Observed measurements

Final verified offline run; these are actual observations, not model-size estimates. Samples every 0.5 seconds can miss brief peaks. Process RSS is not unique physical allocation; shared pages can overlap. No RSS/GPU/available-memory totals are added together.

| Call | Wall seconds | Python peak MiB | Ollama process RSS sum peak GiB | Minimum available GiB | Maximum swap GiB |
|---|---:|---:|---:|---:|---:|
| [ask](../results/runs/20260929T215646-cc492a5e.json) | 17.04 | 34.9 | 2.54 | 1.64 | 6.78 |
| [ask](../results/runs/20260929T215658-ff870f6f.json) | 11.66 | 35.3 | 2.57 | 2.11 | 6.75 |
| [ingest-draft](../results/runs/20260929T215708-c3cd643f.json) | 10.09 | 44.0 | 2.62 | 2.11 | 6.65 |
| [ingest-draft](../results/runs/20260929T215714-2abef8c4.json) | 5.35 | 44.4 | 2.60 | 1.97 | 6.63 |
| [ask](../results/runs/20260929T215726-7655d546.json) | 11.94 | 35.3 | 2.63 | 1.97 | 6.83 |
| [ask](../results/runs/20260929T215739-28f7c4fb.json) | 13.14 | 31.6 | 2.65 | 1.97 | 7.17 |
| [ask](../results/runs/20260929T215750-86b127be.json) | 10.51 | 32.1 | 2.62 | 1.97 | 7.28 |
| [ask](../results/runs/20260929T215753-ba1361b0.json) | 2.57 | 27.6 | 2.57 | 2.61 | 6.70 |
| [chat](../results/runs/20260929T215757-5b7a1aba.json) | 4.05 | 28.1 | 2.60 | 2.66 | 6.30 |
| [chat](../results/runs/20260929T215801-906b038d.json) | 4.70 | 28.1 | 2.60 | 2.69 | 5.46 |
| [chat](../results/runs/20260929T215804-4eb56fee.json) | 2.48 | 28.2 | 2.57 | 2.70 | 4.97 |
| [chat](../results/runs/20260929T215805-09f75d7e.json) | 1.41 | 27.7 | 2.51 | 2.70 | 4.53 |

The first two calls are the same Augustus question: cold after runtime restart, then warm. The first includes model loading; OS disk caches were not flushed. Final Pliny re-ingestion/redrafting took 15.68 seconds end to end. The first-ever Pliny ingestion occurred in the earlier network-interrupted run (68.47 seconds; see results/runs/20260929T170515-40ab429e.json).

Ollama `/api/ps` reported `size=1670350109` and `size_vram=1670350109` bytes with context length 4096. Both describe the same reported model allocation; they are not two physical-RAM pools. This runtime-reported figure is not the downloaded model size or a measurement of total physical memory consumed. The full API response is preserved.

[Machine-readable measurements](measurements.json). Initial connected samples omitted the separate llama-server process; they must not be cited as total inference RSS. The final run includes it. All-app workload changed between runs, so these are not controlled speed benchmarks.
