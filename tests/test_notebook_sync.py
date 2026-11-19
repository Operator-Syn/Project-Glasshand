"""Assert the EDA notebook's embedded modules match ``src/isdm/eda/`` byte for byte.

Why this test exists: the notebook carries its four analysis modules as ``%%writefile`` cells
so it runs on a machine with no ``isdm`` package installed, while the package keeps the
importable source of truth. That is two copies of the same code, and two copies drift. This
test is what makes the duplication safe — edit either side without the other and it fails,
naming the module.

Run with ``uv run python -m pytest tests/test_notebook_sync.py``.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
NOTEBOOK = REPO / "notebooks" / "EDA_Beira_John-Ronan.ipynb"

# (module name as written by the notebook, module file under src/isdm/eda/)
PAIRS = (
    ("eda_quality", "quality.py"),
    ("eda_features", "features.py"),
    ("eda_analysis", "analysis.py"),
    ("eda_viz", "viz.py"),
)


def embedded_source(notebook: Path, module_name: str) -> str:
    """Return the body written by the ``%%writefile`` cell for ``module_name``.

    Args:
        notebook: path to the notebook holding the cells.
        module_name: the module file stem the cell writes, without ``.py``.

    Returns:
        The cell body with the magic line removed and a single trailing newline.

    Raises:
        AssertionError: when no cell writes that module, which means the notebook and this
            test have diverged on naming rather than on content.
    """
    cells = json.loads(notebook.read_text())["cells"]
    marker = f"%%writefile eda_modules/{module_name}.py"

    for cell in cells:
        if cell.get("cell_type") != "code":
            continue
        source = "".join(cell.get("source", []))
        if source.startswith(marker):
            # Drop the magic line; keep everything after it verbatim.
            body = source.split("\n", 1)[1]
            return body.rstrip() + "\n"

    raise AssertionError(f"no %%writefile cell writes eda_modules/{module_name}.py")


@pytest.mark.parametrize(("module_name", "module_file"), PAIRS)
def test_embedded_module_matches_package(module_name: str, module_file: str) -> None:
    """The notebook's copy and the package file must be identical."""
    expected = (REPO / "src" / "isdm" / "eda" / module_file).read_text()
    assert embedded_source(NOTEBOOK, module_name) == expected, (
        f"{module_name} drifted: update the %%writefile cell and src/isdm/eda/{module_file} "
        "together (regenerate the notebook after editing the module)"
    )


def test_notebook_has_no_outputs() -> None:
    """The committed notebook must be output-free, as the Git clean filter enforces."""
    cells = json.loads(NOTEBOOK.read_text())["cells"]
    code_cells = [cell for cell in cells if cell.get("cell_type") == "code"]
    assert code_cells, "notebook has no code cells"
    assert all(not cell.get("outputs") for cell in code_cells), "clear outputs before committing"
    assert all(cell.get("execution_count") is None for cell in code_cells), (
        "execution counts must be null in the committed notebook"
    )
