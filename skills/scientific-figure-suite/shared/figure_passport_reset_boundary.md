# Figure Passport Reset Boundary

## Purpose

Defines the long-session handoff protocol for scientific figure projects. It is
adapted from ARS Material Passport behavior but uses a Figure Passport and
project-local memory.

A reset boundary freezes the current figure state, records the next intended
stage, computes a short hash, and lets the user resume from that hash in a
fresh session without relying on hidden conversational memory.

## Ledger

Boundary and resume entries live in:

```text
.codex/scientific-figure-memory/revision_boundary_ledger.jsonl
```

The ledger is append-only. Prior entries are not deleted, reordered, or mutated.

## Boundary Entry Shape

```json
{
  "kind": "boundary",
  "hash": "000000000000",
  "hash_mode": "SFS_CANONICAL_V1",
  "created_at": "2026-05-19T16:30:00Z",
  "figure_id": "fig_02",
  "from_version": "v1",
  "to_version": "v2",
  "completed_stage": "figure-auditor",
  "next_stage": "export-packager",
  "reason": "Quality audit passed with journal check pending.",
  "artifact_refs": ["figure_passport.json", "quality_audit_history.jsonl"],
  "verification_status": "VERIFIED"
}
```

The placeholder hash is used only during hash computation. The stored entry must
contain the finalized 12-character lowercase SHA-256 prefix.

## Hash Rule

For `SFS_CANONICAL_V1`:

1. Read prior `kind: boundary` entries only. Ignore `kind: resume` entries.
2. Serialize each boundary entry as canonical JSON: sorted keys, UTF-8, compact
   separators, no insignificant whitespace.
3. Serialize the new boundary entry with `hash` equal to
   `"000000000000"`.
4. Concatenate prior boundary serializations and the new placeholder
   serialization, each followed by a single LF byte.
5. SHA-256 the byte stream and use the first 12 lowercase hex characters.
6. Store the finalized hash in the new boundary entry before appending it.

## Reset Tag

When a boundary is created, emit:

```text
[FIGURE-PASSPORT-RESET: hash=<hash>, figure_id=<figure_id>, next=<next_stage>]
```

Also provide a resume instruction:

```text
fig-resume-project resume_from_figure_passport=<hash>
```

## Resume Contract

On `fig-resume-project resume_from_figure_passport=<hash>`:

1. Load `revision_boundary_ledger.jsonl`.
2. Find a `kind: boundary` entry with the matching hash.
3. Refuse to proceed if a later `kind: resume` entry already has
   `consumes_hash` equal to that hash.
4. Warn if `verification_status` is `STALE` or `UNVERIFIED`.
5. Load Figure Passport, project profile, journal targets, datasets, and latest
   audit history by reference.
6. Append a new `kind: resume` entry with `consumes_hash`, timestamp, and chosen
   next stage.
7. Continue from the stored `next_stage` unless the user explicitly overrides it.

## Awaiting Resume

A boundary with hash `H` is awaiting resume when no later resume entry consumes
`H`. This can be computed with one pass over the JSONL ledger.

## Hard Rules

1. Hash mismatch is a hard error.
2. Double-resume is forbidden.
3. Resume does not certify that the figure is ready; quality gates still apply.
4. Boundary hash never includes resume entries.
5. Journal targets remain `ESTIMATED` or `UNVERIFIED` until current guidelines
   are verified in the active task.
6. The reset tag is the machine-stable handoff. Human summary text is not.

