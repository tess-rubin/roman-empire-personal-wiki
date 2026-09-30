# Rubric evidence map

| Requirement | Implementation / evidence |
|---|---|
| Local Gemma, repeatable setup | README setup; scripts/start_ollama.sh; exact identity in run records |
| Persona and separate research instructions | instructions/; romanwiki/harness.py |
| Original sources, source-grounded retrieval | vault/raw/; config/sources.json; SQLite FTS5 in romanwiki/store.py |
| At least five connected notes | Seven reviewed notes in vault/wiki/; grouped vault/index.md; Obsidian screenshots |
| Ingestion and stable note updates | romanwiki/ingest.py; review command; results/reingestion.json |
| Four fixed questions, supporting passages, refusal | expectations.json frozen before implementation; results/evidence-cards/ |
| Chat context isolated from factual evidence | results/mode-review.md; exact mode-check records |
| Offline execution and resource measurement | results/offline-20260929T215623/; results/measurements.md |
| Honest reflection and changes | README reflection; evaluation/changes.md; retained failed runs |
| Public repository and course submission | User publishing instructions in README; not published or submitted |

The first Pliny ingestion happened in an earlier run that later reconnected. The final continuously offline run demonstrates Pliny re-ingestion/redrafting, not first ingestion into an empty index. The MIT HTML presentation is excluded from GitHub and downloaded directly during setup; see THIRD_PARTY_NOTICES.md.
