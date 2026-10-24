#!/data/data/com.termux/files/usr/bin/bash
set -u; . "$(dirname "$0")/common.sh"
emit Q12 ci-fidelity SKIP DEVICE_COMPARISON_REQUIRED 'CI evidence is supplemental and requires device comparison' "platform=$(uname -a)"; exit 2
