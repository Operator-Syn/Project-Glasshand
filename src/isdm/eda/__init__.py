"""Exploratory analysis of the ScreenSpot-Pro Windows subset.

Owns four concerns, one module each:

- :mod:`isdm.eda.quality` — measure completeness, duplication, validity and image integrity.
- :mod:`isdm.eda.features` — derive analysis features and apply the documented cleaning.
- :mod:`isdm.eda.analysis` — summaries and tests quoted in the report.
- :mod:`isdm.eda.viz` — build the report's figures.

These modules are also shipped inside ``notebooks/EDA_Beira_John-Ronan.ipynb`` as
``%%writefile`` cells, so the submitted notebook runs on a machine that has no ``isdm``
package installed — Google Colab included. The notebook copies are byte-for-byte
identical to these files; ``tests/test_notebook_sync.py`` fails when they drift.
"""
