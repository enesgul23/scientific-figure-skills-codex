# Security Policy

## Supported Versions

Security fixes target the latest released version.

## Reporting a Vulnerability

Please report vulnerabilities through GitHub private vulnerability reporting
when available, or open a minimal issue that does not include private data,
tokens, unpublished datasets, patient data, or manuscript-confidential details.

## Data and Privacy Boundary

This repository is a skill package. It must not contain user project memory,
private datasets, credentials, API keys, unpublished manuscript material, or
downloaded external data. Project-local runtime memory belongs under:

```text
.codex/scientific-figure-memory/
```

The `.gitignore` excludes that path by default.
