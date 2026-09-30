#!/bin/bash
# Optional autonomous wrapper. Leaves other networks untouched; runner refuses if any remain.
set -euo pipefail
cd "$(dirname "$0")/.."
DEVICE=$(/usr/sbin/networksetup -listallhardwareports | awk '/Hardware Port: Wi-Fi/{getline; print $2}')
if [ -z "$DEVICE" ]; then echo 'No Wi-Fi interface found; use offline_demo.sh after manual disconnection.'; exit 1; fi
STATE=$(/usr/sbin/networksetup -getairportpower "$DEVICE")
restore() { if [[ "$STATE" == *On ]]; then /usr/sbin/networksetup -setairportpower "$DEVICE" on; fi; }
trap restore EXIT
trap "exit 130" INT TERM
# A detached run must not restore Wi-Fi early if its launching terminal closes.
trap "" HUP
/usr/sbin/networksetup -setairportpower "$DEVICE" off
sleep 4
scripts/offline_demo.sh
