# Notebooks

Working space for isdm. The environment is managed by `uv` from the repository root, so every
notebook runs against the same pinned interpreter and libraries.

## First run

Once per clone, after the repository is synced:

```bash
uv sync
uv run python scripts/setup_notebook_filters.py   # registers the Git clean filter
```

Linux, macOS and Windows are supported: `uv` provisions the interpreter, the setup script is Python
rather than shell, and the filter registers the project interpreter explicitly — `.venv\Scripts\python.exe`
on Windows, `.venv/bin/python` elsewhere.

## Starting a notebook

```bash
uv run jupyter lab --notebook-dir=notebooks
```

Then pick the **Python (isdm)** kernel in the kernel selector, top right of the notebook. The
kernelspec lives inside `.venv/share/jupyter/kernels`, not in your home directory, so it exists only
while you are in this checkout. If the selector offers no such kernel, it was never installed here:

```bash
uv run --frozen python -m ipykernel install --sys-prefix \
  --name isdm --display-name "Python (isdm)"
```

Pick the right kernel before running anything. A notebook run on a different interpreter imports a
different `isdm` or none at all, and the failure looks like a broken package rather than the wrong
kernel. The first cell of `00-workspace-check.ipynb` prints `sys.executable` precisely so that can be
confirmed instead of assumed.

Run cells top to bottom while working. Before handing anything in, run **Kernel → Restart Kernel and
Run All Cells** — a notebook that only works because of state left over from earlier runs is not
reproducible, and for the EDA that check is graded.

Notebooks resolve the repository root themselves (walking up to `pyproject.toml`), so `runs/` lands at
the repo root however Jupyter or `nbconvert` was launched.

### In Google Colab

`EDA_Beira_John-Ronan.ipynb` needs no repository: it writes its analysis modules with `%%writefile`
and imports them from `eda_modules/`. Upload the notebook and the `data/screenspot_pro_windows/`
folder so they sit together in `/content`, then Runtime → Run all. The analysis libraries are already
in Colab's image; if the cleaning-log cell fails on `to_markdown`, run `!pip install tabulate` and
re-run that cell.

### Without the UI

Execution through `nbconvert` is what CI does, and it is how the submitted copies are produced:

```bash
uv run --frozen jupyter nbconvert --to notebook --execute \
  --ExecutePreprocessor.kernel_name=isdm \
  --output-dir runs/eda --output <name>_executed.ipynb notebooks/<name>.ipynb
```

`--ExecutePreprocessor.kernel_name` is not optional: without it nbconvert uses whatever `python3`
resolves to, which is usually not this environment.

## Check the environment

`00-workspace-check.ipynb` prints the interpreter path, library versions and plotting backend, then
writes one synthetic figure to `runs/`. If it runs clean, the workspace is wired correctly.

Run it headlessly, the way CI would. Same command everywhere; only the env-var syntax differs:

```bash
# Linux / macOS
MPLBACKEND=Agg uv run --frozen jupyter nbconvert --to notebook --execute --stdout \
  notebooks/00-workspace-check.ipynb > /dev/null
```

```powershell
# Windows PowerShell
$env:MPLBACKEND="Agg"; uv run --frozen jupyter nbconvert --to notebook --execute --stdout `
  notebooks/00-workspace-check.ipynb > $null
```

## The ScreenSpot-Pro EDA

`EDA_Beira_John-Ronan.ipynb` is the exploratory analysis of the candidate evaluation corpus
(ScreenSpot-Pro, Windows subset). It is a graded submission, so it is deliberately self-contained:
the four analysis modules are written by `%%writefile` cells and imported from `eda_modules/`, which
works in JupyterLab and in Google Colab alike.

```bash
uv run python -m isdm.data.fetch          # downloads data/screenspot_pro_windows (841 MB, resumable)
uv run python -m pytest tests -q          # asserts the notebook's modules match src/isdm/eda/
```

To work on it interactively, start Jupyter as described under [Starting a notebook](#starting-a-notebook)
and pick the **Python (isdm)** kernel. The notebook needs `data/` fetched; it does not need `isdm`
installed, because it carries its own modules.

Execute it and export the submitted copies:

```bash
uv run --frozen jupyter nbconvert --to notebook --execute \
  --ExecutePreprocessor.kernel_name=isdm \
  --output-dir runs/eda --output EDA_Beira_John-Ronan_executed.ipynb \
  notebooks/EDA_Beira_John-Ronan.ipynb

uv run --frozen jupyter nbconvert --to html \
  --output-dir runs/eda --output EDA_Beira_John-Ronan.html \
  runs/eda/EDA_Beira_John-Ronan_executed.ipynb
```

`runs/` is git-ignored, so the committed notebook stays output-free while the executed copy and its
HTML hold every table and figure the submission needs. Do **not** run the export with
`MPLBACKEND=Agg`: the inline backend is what turns `plt.show()` into an embedded figure, and an Agg
run produces a notebook with no plots.

Before submitting, restart the kernel and run all cells in JupyterLab and confirm it finishes with no
errors. The submitted copy is the executed notebook plus its HTML export; the repository copy stays
output-free so diffs show code.

## The grounding and failure analysis

`01-grounding-cart.ipynb` is the integrated analysis of a text-anchored grounding baseline
(RapidOCR + Tesseract, bilingual English/Chinese matching) and the conditions associated with
its request-level outcomes. CART models are evaluated with application-grouped validation; the
same corpus and outcomes support both the grounding metrics and the failure analysis.

The notebook consumes records produced by the runner, so the expensive OCR pass is not
inside a notebook cell:

```bash
uv run python scripts/run_grounding.py --n 1020 \
  --output runs/grounding/records_all.jsonl
uv run python scripts/summarize_grounding.py \
  --records runs/grounding/records_all.jsonl
```

The 300-request balanced pilot is `--per-type 150` with
`--output runs/grounding/records_300.jsonl`; it is a secondary check, not the main run.
The notebook prefers `records_all.jsonl` when it exists.

It needs the system `tesseract` binary, plus the `rapidocr-onnxruntime` and `scikit-learn`
project dependencies. `runs/` is git-ignored; the JSONL records and OCR cache stay local.
The full corpus takes roughly 1.5–2 hours on the first pass; the pilot is ~35–40 minutes.
The summary script writes `runs/grounding/results_summary.md` with the outcome counts,
per-application accuracy, near-miss rates and the CART metrics and rules.

### Windows notes

- Install Tesseract (the UB Mannheim build is the usual Windows option) and add its folder to
  `PATH`. If it is not on `PATH`, set `TESSERACT_CMD` to the full executable path before
  starting Jupyter or the script:
  `set TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe`.
- `uv sync` installs RapidOCR, ONNX Runtime and scikit-learn as normal Windows wheels. The
  OCR cache and JSONL records are written as UTF-8, so the Chinese OCR text survives.
- `nbconvert --to html` needs no LaTeX. Only the EDA PDF export needs MiKTeX or TeX Live.
- The data folder is the same relative path on both systems:
  `data/screenspot_pro_windows/`.

## Git filter

`.gitattributes` routes `*.ipynb` through a clean filter, so outputs and execution counts never reach a
commit and diffs render as readable cells. The attribute rules are committed; the filter *command*
lives in `.git/config` and cannot be, hence `uv run python scripts/setup_notebook_filters.py` once per
clone. The script prints the interpreter it registered, so a wrong one is visible immediately.

Verify with `git check-attr -a -- notebooks/00-workspace-check.ipynb` — it should report
`filter: nbstripout` and `diff: ipynb`. Without the registration git commits unstripped notebooks
without complaining.

## Conventions

- **One notebook per question**, numbered in the order you expect to run them. Later notebooks may
  assume earlier artifacts; say so in a Markdown cell. A notebook that is handed in rather than run
  from the repository follows the naming its course requires instead — `EDA_Beira_John-Ronan.ipynb`
  is `EDA_<Surname>_<FirstName>.ipynb`, not a numbered workspace notebook.
- **Cells hold configuration and calls, nothing else.** Imports, seeds and paths go in one config
  cell; everything after it is a call into `src/isdm/`. A cell that computes is a source file
  that escaped — it cannot be imported, tested or diffed.
  *One documented exception:* `EDA_Beira_John-Ronan.ipynb` is a graded submission that must
  run on a machine with no `isdm` package installed, so it ships its four analysis modules as
  `%%writefile` cells and imports them from `eda_modules/`. `tests/test_notebook_sync.py` keeps
  those copies byte-identical to `src/isdm/eda/`, which is what makes the exception safe. The
  scaffold checker therefore reports two known failures for that notebook
  (`has no %%writefile`, `call cells hold no logic`); they are accepted, not overlooked.
- **The package is organised by concern.** `workspace/` (paths, run layout), `runtime/` (interpreter
  and library introspection), `data/` (loaders, generators, splits), `viz/` (figures, tables). Add a
  subpackage when a new concern arrives, and give each one an `__init__.py` saying what it owns.
- **No `%%writefile`.** Modules under `src/` are ordinary files and the source of truth; generating
  them from cells inverts that ownership and leaves two copies to drift.
- **Outputs are ephemeral.** The Git clean filter strips every output before commit, so a figure or
  table is only real if code wrote it into `runs/`. Display the saved file, not the live object.
- **Keep committed notebooks output-free** (`Cell → All Output → Clear`), so diffs show code.
- **Do not touch a notebook mid-execution** from another process; a kernel writing outputs owns the file.
