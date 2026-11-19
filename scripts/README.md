# Scripts

Notebook plumbing. Two of these run once per clone; the rest are committed so a collaborator
gets the same behaviour as this checkout.

| Script | What it does | When to run it |
|---|---|---|
| `setup_notebook_filters.py` | Writes the `filter.nbstripout` and `diff.ipynb` entries into `.git/config`, pointing at `scripts/nbstripout_safe.py` with `required = true`. | Once per clone, after `uv sync`. Re-run if `.git/config` is lost. |
| `setup_git_hooks.py` | Sets `core.hooksPath` to `scripts/git-hooks`, so the committed `pre-commit` hook runs. | Once per clone. |
| `nbstripout_safe.py` | The clean filter itself. Strips cell outputs and execution counts, and returns `SIGPIPE` to its default so a closed pager does not print a traceback over the diff. | Never by hand — git invokes it. Preflight with `--version`. |
| `git-hooks/pre-commit` | Blocks a commit when `ruff check .` reports errors; reports `ruff format --check` drift and lets the commit through. | Never by hand — git invokes it on `git commit`. Bypass with `--no-verify`. |

Fresh clone:

```bash
uv sync
uv run python scripts/setup_notebook_filters.py
uv run python scripts/setup_git_hooks.py
```

## What is clone-local and why

The attribute rules live in `.gitattributes` and are committed, so every clone routes `*.ipynb`
through the filter. The **filter command and the hooks path live in `.git/config` and cannot be
committed**, because they contain an absolute interpreter path that differs per machine. That is
the entire reason the two setup scripts exist, and why they are not optional.

Never run `nbstripout --install`: it writes one machine's path into the config and every clone
then behaves differently.

## If a file is renamed

`setup_notebook_filters.py` and `setup_git_hooks.py` are the only places the committed filenames
appear. Renaming `nbstripout_safe.py`, `git-hooks/pre-commit`, or this directory without updating
them silently disables the filter or the hook — and a disabled clean filter commits whole
notebooks with their outputs, which is the failure it exists to prevent.

## Verify

```bash
git check-attr -a -- notebooks/00-workspace-check.ipynb   # filter: nbstripout, diff: ipynb
git config --local --get filter.nbstripout.required         # true
git config --local --get core.hooksPath                     # scripts/git-hooks
```
