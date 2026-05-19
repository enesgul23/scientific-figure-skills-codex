---
description: Probe the current Python environment for known figure-rendering libraries without installing them
---

Use `scripts/probe_python_environment.py`. This command checks imports and
versions only; it must not run `pip install` or `conda install`.

Preferred script:

```powershell
python scripts/probe_python_environment.py --out environment_probe.json
```

Use `--library <library_id>` to probe a focused stack.
