#!/data/data/com.termux/files/usr/bin/python
import argparse, hashlib, json, os, pathlib, re, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / 'docs' / 'spike-results'
DEC = ROOT / 'docs' / 'decisions'
DEVICE = os.getenv('TCA_DEVICE_ID', 'sm-t870')
REQUIRED_PHYSICAL_DEVICES = int(os.getenv('TCA_REQUIRED_PHYSICAL_DEVICES', '1'))
DEFER_OK = {
    'Q09': 'NO_MODEL_ENDPOINT',
    'Q11': 'MANUAL_CHECK_REQUIRED',
    'Q12': 'DEVICE_COMPARISON_REQUIRED',
    'Q14': 'SCREEN_OFF_NOT_TESTED',
}
REQUIRED_PKGS = ('starlette', 'uvicorn', 'websockets', 'h11', 'anyio')


def load(path):
    try:
        return json.loads(path.read_text())
    except Exception:
        return None


def file_sha256(path):
    h = hashlib.sha256()
    with path.open('rb') as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def adr_status(number):
    files = sorted(DEC.glob(f'ADR-{number:04d}-*.md'))
    if not files:
        return 'MISSING', None
    match = re.search(
        r'^Status:\s*(\S+)',
        files[0].read_text(errors='replace'),
        re.M,
    )
    return (match.group(1) if match else 'INVALID'), files[0]


def run_command(argv):
    try:
        return subprocess.run(
            argv,
            text=True,
            capture_output=True,
            timeout=30,
        )
    except Exception:
        return None


def validate_device_registry(expected_lock_sha256):
    registry = OUT / 'devices'
    valid = {}
    rejected = []

    for evidence_path in sorted(registry.glob('*/q08.json')):
        result = load(evidence_path)
        rel = str(evidence_path.relative_to(ROOT))

        if result is None:
            rejected.append(f'{rel}: invalid JSON')
            continue

        evidence = result.get('evidence') or {}
        device_id = evidence.get('physical_device_id')
        missing = evidence.get('missing_packages')
        packages = {
            item.get('name'): item.get('version')
            for item in evidence.get('packages', [])
            if isinstance(item, dict)
        }

        checks = {
            'question': result.get('question') == 'Q08',
            'status': result.get('status') == 'PASS',
            'code': result.get('code') == 'DEVICE_INSTALL_OK',
            'physical_device': evidence.get('physical_device') is True,
            'physical_device_id': isinstance(device_id, str) and bool(device_id),
            'lock_sha256': evidence.get('requirements_lock_sha256') == expected_lock_sha256,
            'venv_returncode': evidence.get('venv_returncode') == 0,
            'install_returncode': evidence.get('install_returncode') == 0,
            'pip_check_returncode': evidence.get('pip_check_returncode') == 0,
            'missing_packages': missing == [],
            'required_packages': all(packages.get(name) for name in REQUIRED_PKGS),
        }

        failed = [name for name, passed in checks.items() if not passed]
        if failed:
            rejected.append(f'{rel}: failed checks: {", ".join(failed)}')
            continue

        if device_id in valid:
            rejected.append(
                f'{rel}: duplicate physical_device_id {device_id}; '
                'not counted twice'
            )
            continue

        valid[device_id] = {
            'physical_device_id': device_id,
            'device_slug': evidence.get('device_slug') or evidence_path.parent.name,
            'manufacturer': evidence.get('manufacturer'),
            'model': evidence.get('model'),
            'android_release': evidence.get('android_release'),
            'android_sdk': evidence.get('android_sdk'),
            'architecture': evidence.get('architecture'),
            'python': evidence.get('python'),
            'q08_path': rel,
        }

    return list(valid.values()), rejected


def audit():
    rows = []
    blockers = []
    warnings = []

    for number in range(1, 15):
        question = f'Q{number:02d}'
        path = OUT / f'{DEVICE}-q{number:02d}.json'
        result = load(path) if path.exists() else None
        status, _ = adr_status(number)

        if not path.exists():
            state = 'MISSING'
            code = 'NO_FILE'
            blockers.append(f'{question}: canonical evidence missing')
        elif result is None:
            state = 'INVALID'
            code = 'INVALID_JSON'
            blockers.append(f'{question}: invalid JSON')
        else:
            state = result.get('status', 'INVALID')
            code = result.get('code', 'MISSING_CODE')

            if result.get('question') != question:
                blockers.append(f'{question}: question field mismatch')

            if state == 'PASS' and status != 'Accepted':
                blockers.append(f'{question}: PASS but ADR is {status}')
            elif state == 'SKIP':
                if status == 'Accepted' and DEFER_OK.get(question) == code:
                    warnings.append(f'{question}: accepted deferral {code}')
                else:
                    blockers.append(
                        f'{question}: unresolved SKIP {code}, ADR={status}'
                    )
            elif state not in ('PASS', 'SKIP'):
                blockers.append(f'{question}: result {state}/{code}')

        rows.append((question, state, code, status))

    venv_python = ROOT / '.m0-venv' / 'bin' / 'python'
    venv = 'MISSING'

    if venv_python.exists():
        probe = run_command([
            str(venv_python),
            '-c',
            'import sys; print(int(sys.prefix != sys.base_prefix))',
        ])
        if probe and probe.returncode == 0 and probe.stdout.strip() == '1':
            venv = 'PASS'
        else:
            venv = 'INVALID'

    if venv != 'PASS':
        blockers.append('.m0-venv: missing or not isolated')
    else:
        probe = run_command([str(venv_python), '-m', 'pip', 'check'])
        if not probe or probe.returncode:
            blockers.append('.m0-venv: pip check failed')

        probe = run_command([
            str(venv_python),
            '-c',
            'import starlette,uvicorn,websockets,h11,anyio',
        ])
        if not probe or probe.returncode:
            blockers.append('.m0-venv: required runtime imports failed')

    lock_path = ROOT / 'requirements.lock'
    expected_lock_sha256 = file_sha256(lock_path) if lock_path.exists() else None
    if not expected_lock_sha256:
        blockers.append('requirements.lock: missing')
        devices, rejected_devices = [], []
    else:
        devices, rejected_devices = validate_device_registry(expected_lock_sha256)

    for item in rejected_devices:
        warnings.append(f'device registry rejected: {item}')

    if len(devices) < REQUIRED_PHYSICAL_DEVICES:
        blockers.append(
            'Q08: physical-device coverage '
            f'{len(devices)}/{REQUIRED_PHYSICAL_DEVICES}; '
            f'need {REQUIRED_PHYSICAL_DEVICES - len(devices)} more distinct PASS device(s)'
        )

    matrix = OUT / f'{DEVICE}-q11-manual-matrix.md'
    if not matrix.exists():
        warnings.append('Q11 manual matrix template missing')

    gitignore = ROOT / '.gitignore'
    if (
        not gitignore.exists()
        or '.m0-venv/' not in gitignore.read_text(errors='replace').splitlines()
    ):
        warnings.append('.gitignore missing .m0-venv/')

    review = ROOT / 'M0-REVIEW.md'
    gate_no = (
        review.exists()
        and 'Approved to begin M1: NO' in review.read_text(errors='replace')
    )
    if blockers and not gate_no:
        blockers.append(
            'M0-REVIEW.md must keep Approved to begin M1: NO '
            'while blockers exist'
        )

    return (
        rows,
        blockers,
        warnings,
        venv,
        gate_no,
        devices,
        rejected_devices,
        expected_lock_sha256,
    )


def write_reports(
    rows,
    blockers,
    warnings,
    venv,
    gate_no,
    devices,
    rejected_devices,
    expected_lock_sha256,
):
    data = {
        'device': DEVICE,
        'rows': [
            {'question': q, 'status': s, 'code': c, 'adr': a}
            for q, s, c, a in rows
        ],
        'venv': venv,
        'requirements_lock_sha256': expected_lock_sha256,
        'physical_device_coverage': {
            'required': REQUIRED_PHYSICAL_DEVICES,
            'validated': len(devices),
            'devices': devices,
            'rejected': rejected_devices,
        },
        'blockers': blockers,
        'warnings': warnings,
        'approved_to_begin_m1': not blockers,
    }

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f'{DEVICE}-m0-doctor.json').write_text(
        json.dumps(data, indent=2) + '\n'
    )

    lines = [
        '# M0 Doctor Report',
        '',
        f'- Primary device: `{DEVICE}`',
        f'- Virtual environment: **{venv}**',
        f'- Gate: **{"GO" if not blockers else "NO-GO"}**',
        f'- Physical-device coverage: **{len(devices)}/{REQUIRED_PHYSICAL_DEVICES}**',
        '',
        '## Q/ADR Matrix',
        '',
        '| Q | Result | Code | ADR |',
        '|---|---|---|---|',
    ]
    lines.extend(
        f'| {q} | {s} | `{c}` | {a} |'
        for q, s, c, a in rows
    )
    lines.extend(['', '## Validated Physical Devices', ''])
    if devices:
        for device in devices:
            lines.append(
                f'- `{device["physical_device_id"]}`: '
                f'{device.get("manufacturer") or "?"} '
                f'{device.get("model") or "?"}, '
                f'Android {device.get("android_release") or "?"} '
                f'API {device.get("android_sdk") or "?"}, '
                f'{device.get("architecture") or "?"}'
            )
    else:
        lines.append('- None')
    lines.extend(['', '## Blockers', ''])
    lines.extend([f'- {item}' for item in blockers] or ['- None'])
    lines.extend(['', '## Warnings / Accepted Deferrals', ''])
    lines.extend([f'- {item}' for item in warnings] or ['- None'])

    (OUT / f'{DEVICE}-m0-doctor.md').write_text('\n'.join(lines) + '\n')


def show(rows, blockers, warnings, venv, devices):
    print('=' * 64)
    print('TMUX CODE AGENT - M0 DOCTOR')
    print('=' * 64)
    for q, s, c, a in rows:
        print(f'{q:<4} {s:<7} {c:<34.34} ADR={a}')

    print(f'\n.m0-venv: {venv}')
    print(
        '\nPHYSICAL DEVICE COVERAGE: '
        f'{len(devices)}/{REQUIRED_PHYSICAL_DEVICES}'
    )
    for device in devices:
        print(
            '  [PASS] '
            f'{device["device_slug"]} '
            f'id={device["physical_device_id"]} '
            f'Android={device.get("android_release")} '
            f'API={device.get("android_sdk")} '
            f'arch={device.get("architecture")}'
        )

    print('\nBLOCKERS:')
    for item in blockers:
        print('  [BLOCKED]', item)
    if not blockers:
        print('  [PASS] none')

    print('\nWARNINGS / ACCEPTED DEFERRALS:')
    for item in warnings:
        print('  [INFO]', item)
    if not warnings:
        print('  none')

    print('\nApproved to begin M1:', 'YES' if not blockers else 'NO')
    print(
        'Reports:',
        OUT / f'{DEVICE}-m0-doctor.json',
        OUT / f'{DEVICE}-m0-doctor.md',
    )


def fix():
    changed = []
    gitignore = ROOT / '.gitignore'
    text = gitignore.read_text(errors='replace') if gitignore.exists() else ''
    if '.m0-venv/' not in text.splitlines():
        separator = '' if not text or text.endswith('\n') else '\n'
        gitignore.write_text(text + separator + '.m0-venv/\n')
        changed.append('.gitignore')

    for number in range(1, 15):
        path = OUT / f'{DEVICE}-q{number:02d}.json'
        result = load(path) if path.exists() else None
        if not result:
            continue
        if (
            'runner_exit_code' not in result
            and result.get('status') in ('PASS', 'SKIP')
        ):
            result['runner_exit_code'] = (
                0 if result['status'] == 'PASS' else 2
            )
            changed.append(str(path.relative_to(ROOT)))
        path.write_text(json.dumps(result, indent=2) + '\n')

    print('Mechanical fixes:', ', '.join(changed) if changed else 'none')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=('audit', 'fix', 'gate'))
    args = parser.parse_args()

    if args.mode == 'fix':
        fix()

    result = audit()
    write_reports(*result)
    rows, blockers, warnings, venv, _, devices, _, _ = result
    show(rows, blockers, warnings, venv, devices)

    if args.mode == 'gate':
        raise SystemExit(0 if not blockers else 1)


if __name__ == '__main__':
    main()
