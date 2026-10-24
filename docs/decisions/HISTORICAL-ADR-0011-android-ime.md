# ADR-0011: Android Ime
Status: Proposed

## §44 Question
Q11 — Android IME.

## Evidence
- Device result: `docs/spike-results/sm-t870-q11.json`
- Status: `SKIP`
- Code: `MANUAL_CHECK_REQUIRED`
- Probe exit: `2`
- Summary: Manual Android browser IME checklist required

```json
{
  "text": "Use docs/manual-Q11.md"
}
```

## Draft Decision
Review required. A probe PASS is evidence, not automatic architectural approval. A FAIL or SKIP must be resolved or covered by an explicitly accepted fallback.

## Fallback
Use the fallback stated in §44 of the master design until this ADR is changed from `Proposed` after review.

## Consequences
Document compatibility, security, performance, maintenance, and test effects during review.

## M1 Impact
Keep `Approved to begin M1: NO` until all blocking evidence and the two-device dependency requirement are resolved.
