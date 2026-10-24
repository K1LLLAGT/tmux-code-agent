# ADR-0011: Android IME and Browser Compatibility

Status: Accepted

## §44 Question

Q11: Do the planned CodeMirror editor and xterm.js terminal behave correctly with Android IME composition across the target mobile browsers?

## Evidence

Canonical evidence remains:

- `docs/spike-results/sm-t870-q11.json`
- Result: `SKIP / MANUAL_CHECK_REQUIRED`

Prepared physical-device matrix:

- `docs/spike-results/sm-t870-q11-manual-matrix.md`

Recorded SM-T870 test inventory:

- Android 13 / API 33
- active IME: Samsung Keyboard (`com.samsung.android.honeyboard/.service.HoneyBoardService`)
- Chrome (`com.android.chrome`)
- Samsung Browser (`com.sec.android.app.sbrowser`)
- Tor Browser (`org.torproject.torbrowser`)

The real TCA CodeMirror and xterm.js surfaces do not yet exist in Milestone 0. Therefore no browser/IME combination is marked verified and canonical Q11 remains SKIP.

## Decision

IME/browser compatibility is a device-tested frontend capability, not an assumption derived from browser presence or generic HTML inputs.

When the real frontend surfaces exist, execute the recorded matrix against each supported browser/IME combination. Record editor and terminal results separately.

TCA must not advertise an untested browser/IME combination as verified.

## Fallback

If the configured CodeMirror editor has an IME/composition defect on a supported device/browser, provide a plain textarea editing fallback for basic file editing until the richer editor path is fixed.

If xterm.js terminal input has an IME/composition defect, provide a dedicated mobile terminal input-proxy path that sends committed text/control input to the terminal bridge while retaining xterm.js for rendering.

If a problem is browser-specific, mark that browser combination degraded and direct the user to a verified browser when one exists. Never silently discard, duplicate, or rewrite committed user input.

## Deferred Device Validation

The matrix must eventually cover the recorded operations in `sm-t870-q11-manual-matrix.md`, including composition/autocorrect, deletion, newline, paste, selection/copy, control keys, navigation keys, Unicode, and viewport/keyboard resizing wherever applicable.

The physical-device suite is authoritative for this behavior.

## Consequences

### Positive

- M0 does not claim frontend compatibility before the frontend exists.
- Known classes of mobile IME failure have explicit degraded paths.
- Browser support becomes evidence-based and device-specific.

### Negative

- Canonical Q11 remains deferred until the actual frontend surfaces can be exercised.
- Additional browser/IME combinations require real device testing rather than CI-only approval.

## M1 Impact

ADR-0011 resolves how Q11 is handled before the frontend milestones exist. Canonical Q11 correctly remains `SKIP / MANUAL_CHECK_REQUIRED`.

This accepted deferral does not replace the later physical-device matrix and does not approve M1 by itself.
