# External Data Decision Protocol

## Purpose

Decide whether a scientific figure needs data beyond what the user supplied,
without silently downloading or introducing uncontrolled evidence.

## Default Rule

External data are optional unless the scientific message requires them. Visual
polish, decorative backgrounds, or a desire for a more impressive figure are
not sufficient reasons to add external data.

## Allowed Roles

- `contextual`: basemap, coastline, administrative boundary, or other context
  that helps interpret supplied data but does not by itself support the claim.
- `evidentiary`: external data directly supporting a visual claim.
- `benchmark`: external validation or reference comparison data.
- `annotation`: ontology, pathway, gene set, reference genome metadata, or
  other labels needed to interpret domain-specific measurements.

## Required Provenance

Each external data item must record:

- source name and URL or user-provided file reference
- license
- citation
- access date when obtained
- SHA-256 hash when downloaded or materialized
- usage role
- contamination risk for model-performance or benchmark use

## Decision Gates

1. If no scientific need exists, return `NOT_REQUIRED`.
2. If a need exists but source, license, or citation is missing, return
   `BLOCKED_PENDING_SOURCE`.
3. If provenance is complete, return `RECOMMENDED_WITH_APPROVAL`.
4. If the external data would weaken integrity, violate license constraints, or
   contaminate model evaluation, return `REJECTED`.

## Download Policy

v0.6.0 creates acquisition plans only. It does not download data by default.
Internet downloads require explicit user approval and complete provenance. The
plan must keep `download_allowed: false` until a future execution step is
approved.

## Model-Performance Isolation

External validation or benchmark data must be separated from training,
hyperparameter tuning, early stopping, calibration fitting, and internal
validation. If this cannot be proven, mark contamination risk `high` and block
readiness.
