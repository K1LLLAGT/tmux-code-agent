# ADR-0006: Android Browser Launch

Status: Accepted

## Evidence

- `docs/spike-results/sm-t870-q06.json`
- `docs/spike-results/sm-t870-q06.original-skip.json`

On the SM-T870:

- A temporary HTTP service bound to `127.0.0.1`.
- The loopback test page was reachable.
- `termux-open-url http://127.0.0.1:41876/` returned exit 0.
- The Android browser visibly opened.
- The browser displayed the expected `TCA Q06 PASS` page.
- The temporary server and directory were removed afterward.

## Decision

Use `termux-open-url` as the preferred browser-launch mechanism when
available.

Browser launch is a convenience, not a readiness requirement. The
backend must become READY independently of whether Android accepts the
browser-launch request.

The launcher must always retain and display the authenticated local URL
so the user can open it manually when automatic launch is unavailable.

## Fallback

If `termux-open-url` is absent or unsuccessful:

1. Keep the backend/session running.
2. Print the complete local browser URL clearly.
3. Tell the user that automatic browser launch was unavailable.
4. Offer a clipboard helper when that optional capability is available.
5. Never expose the web service beyond its configured loopback scope
   merely to work around browser-launch failure.

## Consequences

### Positive

- Automatic browser launch works on the tested SM-T870.
- Failure to launch a browser does not destroy or invalidate a session.
- Manual URL opening provides a simple degraded path.

### Negative

- Android background-activity policies may vary by device and OS build.
- Successful command exit alone is insufficient evidence that a browser
  actually appeared, so device tests need manual visual confirmation.

## M1 Impact

Q06 is resolved for the tested SM-T870.

This ADR does not approve Milestone 1 by itself. The remaining M0 gates
must still be completed.
