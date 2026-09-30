import json
import sys
import time
from network_state import state
with open(sys.argv[1],'a',buffering=1) as log:
    while True:
        log.write(json.dumps({'timestamp':time.time(),**state()})+'\n')
        time.sleep(1)
