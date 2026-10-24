#!/data/data/com.termux/files/usr/bin/python
import datetime
import json
import os
import platform
import shutil
import socket
import subprocess
import tempfile
import threading
import time
from pathlib import Path

QUESTION = "Q03"
SPIKE = "private-sshd-auth-matrix"


def command(argv, timeout=15):
    try:
        p = subprocess.run(argv, text=True, capture_output=True, timeout=timeout)
        return {"argv": argv, "returncode": p.returncode,
                "stdout": p.stdout[-8000:], "stderr": p.stderr[-8000:]}
    except subprocess.TimeoutExpired as e:
        return {"argv": argv, "returncode": 124, "timed_out": True,
                "stdout": (e.stdout or "")[-8000:] if isinstance(e.stdout, str) else "",
                "stderr": (e.stderr or "")[-8000:] if isinstance(e.stderr, str) else ""}


def emit(status, code, summary, evidence, exit_code):
    obj = {
        "schema_version": 1,
        "question": QUESTION,
        "spike": SPIKE,
        "status": status,
        "code": code,
        "summary": summary,
        "evidence": evidence,
        "environment": {
            "prefix": os.environ.get("PREFIX"),
            "python": platform.python_version(),
            "platform": platform.platform(),
            "arch": platform.machine(),
        },
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }
    print(json.dumps(obj, separators=(",", ":")))
    raise SystemExit(exit_code)


def free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def wait_port(port, timeout=5.0):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=0.2):
                return True
        except OSError:
            time.sleep(0.1)
    return False


def run_target_server(port, ready, stop):
    with socket.socket() as srv:
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind(("127.0.0.1", port))
        srv.listen(4)
        srv.settimeout(0.2)
        ready.set()
        while not stop.is_set():
            try:
                conn, _ = srv.accept()
            except socket.timeout:
                continue
            with conn:
                conn.sendall(b"TCA_FORWARDING_WORKED")


def ssh_base(port):
    return [
        "ssh", "-F", "none", "-p", str(port),
        "-o", "BatchMode=yes",
        "-o", "StrictHostKeyChecking=no",
        "-o", "UserKnownHostsFile=/dev/null",
        "-o", "GlobalKnownHostsFile=/dev/null",
        "-o", "LogLevel=ERROR",
        "-o", "ConnectTimeout=5",
        "-o", "ConnectionAttempts=1",
    ]


required = ("ssh", "sshd", "ssh-keygen")
missing = [name for name in required if not shutil.which(name)]
if missing:
    emit("FAIL", "MISSING_BINARY", "Required OpenSSH binaries are missing",
         {"missing": missing}, 1)

prefix = os.environ.get("PREFIX")
if not prefix:
    emit("SKIP", "NOT_TERMUX", "PREFIX is not set; target Termux required", {}, 2)

runtime_root = os.environ.get("TMPDIR", os.path.join(prefix, "tmp"))
os.makedirs(runtime_root, exist_ok=True)
sshd_proc = None
forward_proc = None
stop_target = threading.Event()

with tempfile.TemporaryDirectory(prefix="tca-q03-", dir=runtime_root) as td:
    rt = Path(td)
    os.chmod(rt, 0o700)
    port = free_port()
    local_forward_port = free_port()
    target_port = free_port()

    paths = {
        "host": rt / "host_ed25519",
        "good": rt / "exec_ed25519",
        "wrong": rt / "wrong_ed25519",
        "authorized": rt / "authorized_keys",
        "config": rt / "sshd_config",
        "pid": rt / "sshd.pid",
        "server_log": rt / "sshd.log",
    }

    setup = {}
    for label in ("host", "good", "wrong"):
        result = command(["ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-f", str(paths[label])])
        setup[f"keygen_{label}"] = result
        if result["returncode"] != 0:
            emit("FAIL", "KEYGEN_FAILED", f"Failed to generate {label} key", setup, 1)

    good_pub = Path(str(paths["good"]) + ".pub").read_text().strip()
    paths["authorized"].write_text(f'restrict,command="printf forced" {good_pub}\n')
    os.chmod(paths["authorized"], 0o600)

    paths["config"].write_text(f"""Port {port}
ListenAddress 127.0.0.1
AddressFamily inet
HostKey {paths['host']}
PidFile {paths['pid']}
AuthorizedKeysFile {paths['authorized']}
StrictModes no
PubkeyAuthentication yes
PasswordAuthentication no
KbdInteractiveAuthentication no
PermitEmptyPasswords no
AllowTcpForwarding no
AllowStreamLocalForwarding no
AllowAgentForwarding no
X11Forwarding no
PermitTunnel no
PermitUserEnvironment no
PermitUserRC no
PrintMotd no
LogLevel VERBOSE
""")

    config_test = command([shutil.which("sshd"), "-t", "-f", str(paths["config"])])
    effective = command([shutil.which("sshd"), "-T", "-f", str(paths["config"])])
    if config_test["returncode"] != 0:
        emit("FAIL", "SSHD_CONFIG_INVALID", "Private sshd configuration was rejected",
             {"config_test": config_test, "effective": effective}, 1)

    log_handle = paths["server_log"].open("w")
    sshd_proc = subprocess.Popen(
        [shutil.which("sshd"), "-D", "-e", "-f", str(paths["config"])],
        stdout=log_handle, stderr=subprocess.STDOUT, text=True,
    )

    try:
        if not wait_port(port):
            server_log = paths["server_log"].read_text(errors="replace") if paths["server_log"].exists() else ""
            emit("FAIL", "SSHD_NOT_READY", "Private sshd did not become reachable",
                 {"server_log": server_log[-12000:]}, 1)

        base = ssh_base(port)
        key_opts = [
            "-o", "IdentitiesOnly=yes",
            "-o", "PreferredAuthentications=publickey",
            "-o", "PasswordAuthentication=no",
            "-o", "KbdInteractiveAuthentication=no",
        ]

        positive = command(base + key_opts + ["-i", str(paths["good"]), "127.0.0.1", "ignored"])
        wrong_key = command(base + key_opts + ["-i", str(paths["wrong"]), "127.0.0.1", "ignored"])
        no_key = command(base + [
            "-o", "IdentitiesOnly=yes", "-o", "IdentityFile=none",
            "-o", "PubkeyAuthentication=no",
            "-o", "PasswordAuthentication=no",
            "-o", "KbdInteractiveAuthentication=no",
            "-o", "PreferredAuthentications=none",
            "127.0.0.1", "ignored",
        ])
        password = command(base + [
            "-o", "IdentitiesOnly=yes", "-o", "IdentityFile=none",
            "-o", "PubkeyAuthentication=no",
            "-o", "KbdInteractiveAuthentication=no",
            "-o", "PreferredAuthentications=password",
            "-o", "NumberOfPasswordPrompts=0",
            "127.0.0.1", "ignored",
        ])
        pty = command(base + key_opts + ["-tt", "-i", str(paths["good"]), "127.0.0.1", "ignored"])

        target_ready = threading.Event()
        target_thread = threading.Thread(
            target=run_target_server,
            args=(target_port, target_ready, stop_target), daemon=True,
        )
        target_thread.start()
        if not target_ready.wait(2):
            emit("FAIL", "TARGET_SERVER_FAILED", "Forwarding target could not start", {}, 1)

        forward_stderr = rt / "forward.stderr"
        with forward_stderr.open("w") as ferr:
            forward_proc = subprocess.Popen(
                base + key_opts + [
                    "-i", str(paths["good"]),
                    "-N", "-L", f"127.0.0.1:{local_forward_port}:127.0.0.1:{target_port}",
                    "-o", "ExitOnForwardFailure=yes",
                    "127.0.0.1",
                ],
                stdout=subprocess.DEVNULL, stderr=ferr, text=True,
            )

        local_listener_appeared = wait_port(local_forward_port, timeout=2.0)
        forwarding_token = b""
        forwarding_error = ""
        if local_listener_appeared:
            try:
                with socket.create_connection(("127.0.0.1", local_forward_port), timeout=2) as client:
                    client.settimeout(2)
                    forwarding_token = client.recv(128)
            except OSError as e:
                forwarding_error = repr(e)
        time.sleep(0.3)
        if forward_proc.poll() is None:
            forward_proc.terminate()
            try:
                forward_proc.wait(timeout=2)
            except subprocess.TimeoutExpired:
                forward_proc.kill()
                forward_proc.wait(timeout=2)
        forward_text = forward_stderr.read_text(errors="replace") if forward_stderr.exists() else ""

        effective_text = effective.get("stdout", "").lower()
        checks = {
            "correct_key_forced_command": positive["returncode"] == 0 and positive["stdout"] == "forced",
            "wrong_key_rejected": wrong_key["returncode"] != 0,
            "no_key_rejected": no_key["returncode"] != 0,
            "password_rejected": password["returncode"] != 0,
            "pty_rejected": (
                pty["returncode"] != 0
                or "pty allocation request failed" in pty["stderr"].lower()
            ),
            "tcp_forwarding_rejected": forwarding_token != b"TCA_FORWARDING_WORKED",
            "loopback_configured": "listenaddress 127.0.0.1" in effective_text,
            "server_tcp_forwarding_disabled": "allowtcpforwarding no" in effective_text,
            "server_agent_forwarding_disabled": "allowagentforwarding no" in effective_text,
            "server_password_disabled": "passwordauthentication no" in effective_text,
            "server_kbdinteractive_disabled": "kbdinteractiveauthentication no" in effective_text,
        }

        server_log = paths["server_log"].read_text(errors="replace") if paths["server_log"].exists() else ""
        evidence = {
            "port": port,
            "config_test": config_test,
            "effective_config_selected": [
                line for line in effective.get("stdout", "").splitlines()
                if line.lower().startswith((
                    "listenaddress ", "pubkeyauthentication ", "passwordauthentication ",
                    "kbdinteractiveauthentication ", "allowtcpforwarding ",
                    "allowagentforwarding ", "x11forwarding ", "permittunnel ",
                    "strictmodes ", "authorizedkeysfile ",
                ))
            ],
            "checks": checks,
            "correct_key": positive,
            "wrong_key": wrong_key,
            "no_key": no_key,
            "password": password,
            "pty": pty,
            "forwarding": {
                "local_listener_appeared": local_listener_appeared,
                "received": forwarding_token.decode(errors="replace"),
                "client_error": forwarding_error,
                "ssh_stderr": forward_text[-8000:],
            },
            "server_log": server_log[-12000:],
        }

        failed = [name for name, ok in checks.items() if not ok]
        if failed:
            emit("FAIL", "AUTH_MATRIX_FAILED", "One or more SSH authentication/restriction checks failed",
                 {**evidence, "failed_checks": failed}, 1)
        emit("PASS", "AUTH_MATRIX_OK", "Private Termux sshd authentication and restriction matrix passed",
             evidence, 0)
    finally:
        stop_target.set()
        if forward_proc is not None and forward_proc.poll() is None:
            forward_proc.terminate()
        if sshd_proc is not None and sshd_proc.poll() is None:
            sshd_proc.terminate()
            try:
                sshd_proc.wait(timeout=2)
            except subprocess.TimeoutExpired:
                sshd_proc.kill()
                sshd_proc.wait(timeout=2)
        log_handle.close()
