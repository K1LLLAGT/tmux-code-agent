#!/data/data/com.termux/files/usr/bin/python

import datetime
import json
import os
import platform
from importlib import metadata

QUESTION = "Q13"
SPIKE = "license-audit"

PACKAGES = (
    "starlette",
    "uvicorn",
    "websockets",
    "h11",
    "anyio",
)

packages = []
blocking = []

for name in PACKAGES:
    try:
        dist = metadata.distribution(name)
    except metadata.PackageNotFoundError:
        packages.append(
            {
                "name": name,
                "version": None,
                "license": "NOT_INSTALLED",
                "source": None,
            }
        )
        blocking.append(name)
        continue

    legacy = dist.metadata.get("License")
    expression = dist.metadata.get("License-Expression")

    classifiers = dist.metadata.get_all("Classifier") or []

    license_classifiers = [
        item
        for item in classifiers
        if item.startswith("License ::")
    ]

    if expression:
        license_value = expression.strip()
        source = "License-Expression"
    elif legacy and legacy.strip():
        license_value = legacy.strip()
        source = "License"
    elif license_classifiers:
        license_value = "; ".join(license_classifiers)
        source = "Classifier"
    else:
        license_value = "UNKNOWN"
        source = None
        blocking.append(name)

    packages.append(
        {
            "name": name,
            "version": dist.version,
            "license": license_value,
            "source": source,
            "license_expression": expression,
            "legacy_license": legacy,
            "license_classifiers": license_classifiers,
        }
    )

status = "PASS" if not blocking else "FAIL"
code = "LICENSE_METADATA_OK" if not blocking else "UNKNOWN_OR_MISSING"

result = {
    "schema_version": 1,
    "question": QUESTION,
    "spike": SPIKE,
    "status": status,
    "code": code,
    "summary": (
        "Installed dependency license metadata was recorded "
        "without guessing"
    ),
    "evidence": {
        "packages": packages,
        "blocking": blocking,
    },
    "environment": {
        "prefix": os.environ.get("PREFIX"),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "arch": platform.machine(),
        "android_sdk": os.popen(
            "getprop ro.build.version.sdk 2>/dev/null"
        ).read().strip(),
    },
    "timestamp": datetime.datetime.now(
        datetime.timezone.utc
    ).isoformat(),
}

print(json.dumps(result, separators=(",", ":")))

raise SystemExit(0 if status == "PASS" else 1)
