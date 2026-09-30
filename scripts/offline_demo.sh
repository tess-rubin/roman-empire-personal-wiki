#!/bin/bash
# Standalone, no internet calls. Disconnect manually before launching this runner.
set -u
cd "$(dirname "$0")/.." || exit 1
RUN="results/offline-$(date +%Y%m%dT%H%M%S)"
mkdir -p "$RUN"
exec > >(tee "$RUN/terminal.txt") 2>&1
set -x
.venv/bin/python scripts/network_state.py > "$RUN/network-before.json"
cat "$RUN/network-before.json"
if ! .venv/bin/python -c 'from scripts.network_state import state; import sys; sys.exit(not state()["offline"])'; then
  echo 'OFFLINE PROOF FAILED: disconnect Wi-Fi, Ethernet, tethering and VPN; rerun. No Pliny ingestion attempted.'
  exit 3
fi
.venv/bin/python scripts/network_monitor.py "$RUN/network-samples.jsonl" &
MONITOR_PID=$!
# Restart only the assignment-specific server (matched by its listening port).
PID=$(/usr/sbin/lsof -tiTCP:11435 -sTCP:LISTEN)
if [ -n "$PID" ]; then kill "$PID"; sleep 3; fi
scripts/start_ollama.sh > "$RUN/ollama.log" 2>&1 &
SERVER_PID=$!
trap 'kill "$SERVER_PID" "$MONITOR_PID" 2>/dev/null || true' EXIT
sleep 5
./wiki help
.venv/bin/python - <<'PY'
from romanwiki.runtime import snapshot,identity
import json
print(json.dumps({'baseline':snapshot(),'model':identity()},indent=2))
PY
# Separate CLI processes prove restart; first model call after restart is cold.
./wiki ask 'According to Augustus, how did his power compare with his colleagues after his sixth and seventh consulships?'
./wiki ask 'According to Augustus, how did his power compare with his colleagues after his sixth and seventh consulships?'
./wiki ingest vault/raw/pliny.html --redraft
INGEST_STATUS=$?
.venv/bin/python scripts/evaluate.py --label offline
EVAL_STATUS=$?
.venv/bin/python -m unittest discover -s tests -v
TEST_STATUS=$?
# Search really runs with the assignment runtime stopped.
kill "$SERVER_PID"
wait "$SERVER_PID" || true
./wiki search 'Nicomedia aqueduct'
SEARCH_STATUS=$?
./wiki ask 'Nicomedia aqueduct'
ERROR_STATUS=$?
.venv/bin/python scripts/network_state.py > "$RUN/network-after.json"
cat "$RUN/network-after.json"
kill "$MONITOR_PID"
wait "$MONITOR_PID" 2>/dev/null || true
.venv/bin/python - "$RUN" "$INGEST_STATUS" "$EVAL_STATUS" "$TEST_STATUS" "$SEARCH_STATUS" "$ERROR_STATUS" <<'PY'
import json,sys
from pathlib import Path
p=Path(sys.argv[1]);codes=dict(zip(['ingest','eval','unit','stopped_search','stopped_ask'],map(int,sys.argv[2:])))
samples=[json.loads(line) for line in (p/'network-samples.jsonl').read_text().splitlines()]
result={'continuous_offline':bool(samples) and all(s['offline'] for s in samples),'network_sample_count':len(samples),'exit_codes':codes,'network_before':json.loads((p/'network-before.json').read_text()),'network_after':json.loads((p/'network-after.json').read_text()),'claim_review':'PENDING independent assessment'}
(p/'runner-summary.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
sys.exit(not (result['continuous_offline'] and result['network_after']['offline'] and codes=={'ingest':0,'eval':0,'unit':0,'stopped_search':0,'stopped_ask':2}))
PY
SUMMARY_STATUS=$?
set +x
echo "Offline runner finished. Evidence: $RUN. Review draft notes with ./wiki review KEY --approve after checking their claims."

exit "$SUMMARY_STATUS"
