# fig-doctor

Inspect the local Scientific Figure Suite environment without installing
packages or changing project memory.

```bash
python scripts/probe_python_environment.py --library pandas --library numpy --library matplotlib
python scripts/validate_render_template_registry.py
python scripts/validate_library_pool.py
python scripts/validate_memory.py --memory-dir tests/sample_memory/scientific-figure-memory
```

For shell users, run:

```bash
bash scripts/bin/sfs-doctor.sh
```
