"""Data loading / answer-key handling helpers for the GBM-Space Level 1 & Level 2 notebooks."""

from __future__ import annotations

from pathlib import Path

import anndata as ad
import pandas as pd

# .obs columns in the provided snRNA-seq data that encode ground-truth annotations the
# students are meant to reconstruct themselves. Stripped from student-facing files by
# scripts/01_prepare_snrna_subset.py and kept only in the instructor answer key.
SNRNA_ANSWER_KEY_OBS_COLUMNS = [
    "cell_status",
    "annotation_coarse",
    "annotation_granular",
    "neftel",
    "celltypist",
    "scPoli",
    "ontology keywords",
    "top_markers",
    "CNV_signal_mean",
    "cnv_corr",
    "phase",
]

# Precomputed embeddings/graphs to strip so students compute their own.
SNRNA_ANSWER_KEY_OBSM_KEYS = ["X_umap"]
SNRNA_ANSWER_KEY_OBSP_KEYS = ["connectivities", "distances"]
SNRNA_ANSWER_KEY_UNS_KEYS = ["hvg"]

# Visium .var['feature_types'] categories that are pre-computed results (cell2location /
# niche-NMF / IvyGAP histopathology overlap) rather than raw gene expression. Stripped from
# student-facing Visium files; kept as the Level 2 answer key / checkpoint reference.
VISIUM_ANSWER_KEY_FEATURE_TYPES = [
    "Cell state abundances",
    "Spatial niche abundances",
    "Histopath annotation overlap",
]


def split_snrna_answer_key(adata: ad.AnnData) -> tuple[ad.AnnData, pd.DataFrame]:
    """Return (student_adata, answer_key_df). Does not mutate `adata` in place."""
    present_cols = [c for c in SNRNA_ANSWER_KEY_OBS_COLUMNS if c in adata.obs.columns]
    answer_key = adata.obs[present_cols].copy()

    student = adata.copy()
    student.obs = student.obs.drop(columns=present_cols)
    for key in SNRNA_ANSWER_KEY_OBSM_KEYS:
        student.obsm.pop(key, None)
    for key in SNRNA_ANSWER_KEY_OBSP_KEYS:
        student.obsp.pop(key, None)
    for key in SNRNA_ANSWER_KEY_UNS_KEYS:
        student.uns.pop(key, None)
    return student, answer_key


def split_visium_answer_key(adata: ad.AnnData) -> tuple[ad.AnnData, ad.AnnData]:
    """Return (student_adata, answer_key_adata) split by `var['feature_types']`.
    Both keep the same `.obs`/`.obsm['spatial']`/`.uns['spatial']` (image) — only `.var`/`.X`
    columns differ, since cell2location/niche/histopath results are stored as extra
    "genes" sharing the same expression matrix in the provided data.
    """
    is_answer_key = adata.var["feature_types"].isin(VISIUM_ANSWER_KEY_FEATURE_TYPES)
    student = adata[:, ~is_answer_key].copy()
    answer_key = adata[:, is_answer_key].copy()
    return student, answer_key


def load_level1_reference(data_dir: str | Path) -> ad.AnnData:
    """Load the Level 1 solution's saved, annotated AT10+AT14 reference for use as the
    cell2location signature input in Level 2. Kept as a tiny indirection so the path lives
    in one place.
    """
    data_dir = Path(data_dir)
    return ad.read_h5ad(data_dir / "level1_snrna_AT10_AT14_annotated.h5ad")
