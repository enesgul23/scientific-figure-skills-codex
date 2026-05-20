# Shared Contracts

JSON schemas for major scientific figure suite handoff artifacts. These schemas
are intentionally lightweight: they catch missing required fields and status
enum drift while leaving room for domain-specific extensions.

Memory contracts cover project-local `.codex/scientific-figure-memory/`
artifacts. The schemas belong to the installed skill; real project memory does
not.

v0.6 contracts add Library Intelligence Runtime artifacts: library pool
metadata, dependency plans, data acquisition plans, and renderer dependency
metadata. These are planning and validation artifacts only; they do not install
packages or download external data.

v0.7 contracts add multi-panel layout audit artifacts for optical-grid,
colorbar, semantic color, and direct-label checks.

v0.8 contracts add text layout reports and bundled domain text profiles for
overlap, clipping, colorbar-title, direct-label, and terminology checks.

Use with:

```powershell
python scripts/validate_contracts.py .
```
