# ADR-0007: Starlette and Uvicorn Web Stack

Status: Accepted

## §44 Question

Q07: Is the candidate pure-Python Starlette, Uvicorn, h11,
WebSockets, and AnyIO stack functional and sufficiently lightweight
on the target Termux device?

## Evidence

Primary evidence:

- `docs/spike-results/sm-t870-q07.json`
- `docs/spike-results/sm-t870-q07-live-web-rss.json`
- `docs/spike-results/sm-t870-q07-isolated-imports.json`
- `docs/spike-results/sm-t870-m0-venv-import-check.txt`
- `docs/spike-results/sm-t870-m0-venv-freeze.txt`

Historical evidence:

- `docs/spike-results/sm-t870-q07.global-python-failure.json`
- `docs/spike-results/sm-t870-q07.original-global-failure.json`

Test environment:

- Android 13 / API 33
- aarch64
- Python 3.14.8
- Isolated `.m0-venv`
- Starlette 1.9.0
- Uvicorn 0.54.0
- WebSockets 17.3
- h11 0.16.0
- AnyIO 4.15.1

Verified behavior:

- All candidate packages imported successfully in the isolated environment.
- Uvicorn started with one worker.
- The server bound only to `127.0.0.1`.
- A Starlette `/health` endpoint became ready.
- Twenty-one loopback health requests returned HTTP 200.
- Idle Uvicorn RSS remained at 34,304 KiB across ten samples.
- RSS after the request sequence was 34,344 KiB.
- The server process terminated cleanly.
- No Q07 temporary runtime directory remained.

The observed web-stack RSS is below the design target of 120 MiB
idle daemon RSS.

## Decision

Use Starlette with Uvicorn for the TCA backend and local web server.

Use:

- one Uvicorn worker per TCA session
- loopback-only binding
- explicit readiness through `/health`
- the isolated project-owned Python environment
- pinned dependencies from `requirements.lock`
- no development reload mode in production
- bounded request, event, and WebSocket queues
- supervisor-managed shutdown and cleanup

The runtime must not depend on Starlette or Uvicorn being installed in
the user's global Termux Python environment.

## Fallback

If a future dependency lock, device class, or soak test exceeds the
approved resource budget:

1. Re-run the live Q07 health and RSS probe.
2. Reduce optional middleware and instrumentation.
3. Evaluate a smaller pure-Python ASGI/WebSocket stack.
4. Keep the same loopback binding, authentication, and health semantics.
5. Record any stack replacement or budget revision in a new ADR.

## Consequences

### Positive

- The complete candidate web stack works on the tested Termux device.
- The measured memory footprint is within the current idle target.
- The stack uses the project's isolated dependency environment.
- Loopback health and cleanup are automatically testable.

### Negative

- The web stack contributes roughly 34 MiB of resident memory before
  the remaining daemon subsystems and model server are included.
- Dependency changes require repeated install, license, health, RSS,
  and cleanup tests.
- A full-session soak test is still required during later milestones.

## M1 Impact

Q07 is resolved for the tested SM-T870 and dependency lock.

This ADR does not approve Milestone 1 by itself. The complete M0 gate,
including remaining manual questions and the second-device install,
remains open.
