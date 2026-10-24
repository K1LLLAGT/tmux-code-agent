#!/data/data/com.termux/files/usr/bin/bash
set -u; . "$(dirname "$0")/common.sh"
is_termux || { emit Q03 private-sshd SKIP NOT_TERMUX 'Target Termux required' ''; exit 2; }
for c in ssh sshd ssh-keygen python; do command -v "$c" >/dev/null || { emit Q03 private-sshd FAIL MISSING_BINARY "$c missing" ''; exit 1; }; done
rt=$(mktemp -d "${TMPDIR:-$PREFIX/tmp}/tca-sshd.XXXXXX"); pid=''; trap '[ -n "$pid" ] && kill "$pid" 2>/dev/null || true; rm -rf "$rt"' EXIT
port=$(python -c 'import socket;s=socket.socket();s.bind(("127.0.0.1",0));print(s.getsockname()[1]);s.close()')
ssh-keygen -q -t ed25519 -N '' -f "$rt/host";ssh-keygen -q -t ed25519 -N '' -f "$rt/exec"
printf 'restrict,command="printf forced" %s\n' "$(cat "$rt/exec.pub")" >"$rt/authorized_keys"
cat >"$rt/sshd_config" <<EOF
Port $port
ListenAddress 127.0.0.1
HostKey $rt/host
PidFile $rt/sshd.pid
AuthorizedKeysFile $rt/authorized_keys
PubkeyAuthentication yes
StrictModes no
PasswordAuthentication no
KbdInteractiveAuthentication no
AllowTcpForwarding no
AllowAgentForwarding no
X11Forwarding no
PermitTunnel no
EOF
"$(command -v sshd)" -D -e -f "$rt/sshd_config" 2>"$rt/sshd.log" & pid=$!
sleep 1
out=$(ssh -F none -p "$port" -i "$rt/exec" -o IdentitiesOnly=yes -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o BatchMode=yes 127.0.0.1 ignored 2>"$rt/ssh-client.log"); rc=$?
if [ "$rc" -eq 0 ] && [ "$out" = forced ]; then emit Q03 private-sshd PASS FORCED_COMMAND_OK 'Private non-root sshd forced command succeeded' "port=$port"; else emit Q03 private-sshd FAIL SSH_MATRIX_FAILED 'Private sshd test failed' "rc=$rc out=$out log=$(cat "$rt/sshd.log")"; exit 1; fi
