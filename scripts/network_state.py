#!/usr/bin/env python3
"""Record interface state without exposing addresses or device identifiers."""
import json
import subprocess
import psutil

def state():
    active=[]
    for name,stats in psutil.net_if_stats().items():
        if stats.isup and name!='lo0':
            addrs=psutil.net_if_addrs().get(name,[])
            routable=any(a.family.name in ['AF_INET','AF_INET6'] and not a.address.startswith(('fe80:','127.','::1')) for a in addrs)
            if routable:active.append(name)
    route=subprocess.run(['/sbin/route','-n','get','default'],capture_output=True,text=True)
    # Store only interface/no-route signal, not gateway addresses.
    route_interface=next((l.split(':',1)[1].strip() for l in route.stdout.splitlines() if 'interface:' in l),None)
    return {'active_nonloopback_ip_interfaces':active,'default_route_interface':route_interface,'offline':not active and route_interface is None}
if __name__=='__main__':print(json.dumps(state(),indent=2))
