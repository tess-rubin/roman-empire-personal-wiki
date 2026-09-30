# Failures and changes

Expectations were frozen before retrieval implementation; see freeze.json. Expected original passages are stored outside the searchable corpus.

## Connected smoke attempt 1

- Rebuilding Rome draft joined separated source sentences into one quotation. Citation validation correctly rejected it (results/runs/20260929T165617-9c1a8011.json). Also, “property rights” and the description of a country residence were interpretive overreach; reviewed notes remove these.
- Source indexing originally occurred after every draft succeeded. As a consequence, Tacitus was absent from FTS after that draft failure. The Nero smoke answer cited Augustus on a different question. This is a failed answer despite a valid quote.
- Change: validated source extraction/indexing now commits independently before drafting. Drafts remain excluded from evidence. Research instructions require contiguous quotes from one passage, narrower claims, named-author attribution and relevance to the requested person.
- Rerun required: Tacitus ingestion and both connected question tests, then the full offline suite.
- Editorial review: preserve Augustus’s self-presentation, distinguish rank from office power, attribute the appended summary, remove an unsupported characterization of spectacles as military expenditure. Original model outputs are retained.

## Connected smoke attempt 2

Retrieval recovered Tacitus 39 and the Nero answer covered all required relief measures (plus two supported rebuilding details). Augustus retrieved chapter 34, but the answer omitted precedence in rank: **incomplete**, despite a cited full passage. The follow-up prompt now explicitly requests complete comparisons, named-author attribution, focused claims, and short contiguous quotes. This is general guidance, not an answer-key lookup. Rerun Augustus, then all four questions offline. Memory sampling now includes the separate `llama-server` process, which Ollama 0.34.3 uses for inference; initial samples omitted that child and must not be interpreted as total model RSS.

## Connected smoke attempt 3

The Augustus answer still omitted rank and incorrectly paraphrased equal power as “power remained with his colleagues.” Retained in connected-augustus-final.txt; **fail**, not final success despite the filename. Added explicit historical-precision rules distinguishing rank/prestige from formal office powers and rejecting that misleading paraphrase. This prompt change was informed by the failed evaluation; expectations remain unchanged. The offline suite is the next full retest.

## First offline attempt

Network was off at the initial checkpoint but active at the final checkpoint; this attempt is **not complete offline proof**. Pliny's first ingestion occurred in this run; the exact moment of reconnection was not measured. The full run and its failed outputs remain in results/offline-20260929T170219 and results/offline-20260929T170516.

Augustus now states the rank/power contrast. Nero failed exact-quote validation. The unsupported response omitted required `claims`, which was correctly recorded as malformed rather than silently normalized. Pliny's output confused Trajan’s reply with Pliny and assigned an unrelated Augustus restoration to Trajan: **semantic failure** despite quote validity.

Changes: add explicit speaker attribution to retrieved evidence (including alternating Pliny/Trajan letters), scope retrieval to explicitly named authors/emperors while allowing multiple named sources, and constrain Ollama with a JSON schema requiring all fields. Add one logged repair attempt for invalid model citations/schema, preserving the original failure. Add continuous network sampling to the standalone runner and make an interrupted connection-free interval fail the offline-proof check. No expected answer text is supplied to inference.

## Second offline attempt

All automatic retrieval/status/citation checks passed, but continuous monitoring found Wi-Fi active after the opening interval (24 offline samples out of 271). It remains a **local run with failed offline proof**. Independent review found the Nero summary omitted temporary shelters even though its displayed supporting quotation included them; it also spent claims on later rebuilding. Added general completeness guidance to prioritize directly relevant actions before background. User subsequently confirmed they can leave all connections off for the final run.

## Final verification and documentation

Final offline runner recorded 101 offline samples, successful evaluation and expected stopped-runtime behavior. Evidence cards now contain separate claim assessment. Obsidian navigation/source opening and seven-node graph verified. Post-run changes improve local source attachment links, handle unavailable memory metrics without aborting, and allow renamed related-note titles during drafting; inference settings and evidence selection are unchanged. Reviewed note checksums refreshed after source-link edits.

## Publication preparation

MIT HTML excluded from distribution; unchanged direct-download setup remains checksum verified. Local home-directory paths redacted in published records; originals retained privately. No source passages, inference settings, or measured results changed.
