# ADR-0010: Filesystem Primitives and Storage Scope

Status: Accepted

## Evidence
- `docs/spike-results/sm-t870-q10.json`
- Result: `PASS / PRIVATE_STORAGE_OK`

## Decision
Use the hardened filesystem primitives only where the runtime probe confirms the required semantics. Treat Termux private/internal storage as the fully supported default scope on the tested device. Shared-storage behavior must remain separately detected and restricted when equivalent guarantees cannot be demonstrated.

## Fallback
For storage that cannot provide the required dir-fd, no-follow, and related containment semantics, enter restricted shared-storage mode: avoid claiming race-resistant containment, limit writes/operations accordingly, and surface the restriction to the user.

## Consequences
Q10 establishes the required private-storage path for the tested SM-T870. It does not justify assuming identical semantics on Android shared/FUSE storage.

## M1 Impact
The private-storage prerequisite is resolved for the tested device. Shared-storage restrictions remain part of later filesystem implementation/testing, while the overall M0 gate remains open.
