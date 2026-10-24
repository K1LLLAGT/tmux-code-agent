#!/data/data/com.termux/files/usr/bin/bash
set -u; . "$(dirname "$0")/common.sh"
is_termux || { emit Q08 dependency-install SKIP NOT_TERMUX 'Target Termux required' ''; exit 2; }
[ -f requirements.lock ] || { emit Q08 dependency-install FAIL LOCK_MISSING 'requirements.lock missing' ''; exit 1; }
rt=$(mktemp -d "${TMPDIR:-$PREFIX/tmp}/tca-venv.XXXXXX"); trap 'rm -rf "$rt"' EXIT
python -m venv "$rt/v" || { emit Q08 dependency-install FAIL VENV_FAILED 'Unable to create disposable venv' ''; exit 1; }
log=$rt/pip.log; "$rt/v/bin/pip" install -r requirements.lock >"$log" 2>&1; rc=$?
if [ "$rc" -eq 0 ]; then emit Q08 dependency-install PASS INSTALL_OK 'Candidate dependencies installed in a disposable venv' "$(tail -n 30 "$log")"; else emit Q08 dependency-install FAIL INSTALL_FAILED 'Candidate install failed' "$(tail -n 60 "$log")"; exit 1; fi
