# Build Notes (instructor-facing — not for students)

Working notes from building this project, for future maintainers (or future-me).
Source paper: de Jong, Memi, Gracia, Lazareva et al., *"A spatiotemporal cancer cell
trajectory underlies glioblastoma heterogeneity"*, bioRxiv 2025.05.13.653495.
gbmspace.org. SpaceTree code: github.com/PMBio/spaceTree.

## Donor / sample selection

- 12 donors total in the cohort (AT3-AT15, no AT1/AT2/AT8 ever existed in this study).
  Every donor has *some* snRNA-seq + Visium coverage.
- **Used: AT10 + AT14 only**, all cells, no subsampling (118,471 cells: AT10=85,983,
  AT14=32,488). Originally considered AT10+AT14+AT15, but:
  - `data/snRNA_seq/donor_split/AT15.h5ad` is **HDF5-corrupted** ("bad object header
    version number", confirmed via h5py with multiple drivers — not a permissions issue).
    AT15's data is still recoverable by slicing the 62GB combined `GBM_space_snRNA.h5ad`,
    but wasn't worth the complexity for the gain. **TODO: flag this file for regeneration
    to whoever maintains the shared data folder** — independent of whether we ever use
    AT15, it's just broken and should be fixed at the source.
  - AT15's Visium sections use a different chemistry (CytAssist-style, ~half the gene
    panel, ~3x the spot count) than AT10/AT14's standard Visium — would've introduced a
    confusing technical confound for a teaching cell2location exercise.
  - AT15 is also heavily skewed toward NPC-neuronal-like (42% of its own malignant cells)
    — AT10+AT14 alone already cover all 18 `annotation_coarse` categories without that skew.
- Visium: `anndata_selected/` (9 sections total) is *already* curated down to exactly
  AT10 (5 sections) + AT14 (1 section) + AT15 (3 sections) — i.e. whoever prepared this
  folder for the course already encoded the same matched-donor logic. We use:
  - **Primary**: `AT10-BRA-5-FO-1_2` (3,999 spots, full cell2location/niche/histopath
    answer-key features present).
  - **Optional secondary**: `AT14-BRA-4-FO-2_1` (3,534 spots, no IvyGAP histopath overlap
    feature — flag this if it's used).

## Data quirks found during prep

- `.X` and `.raw.X` in the provided snRNA files are both **raw integer counts** (confirmed
  via h5py, not documented explicitly in the README) — standard normalize/log1p workflow
  applies as-is.
- snRNA `.obs` column names are **lowercase** (`cell_status`, `top_markers`) even though
  the README documents them title-cased (`Cell_status`, `Top_markers`) — caught this via
  a leaky first run of `scripts/01_prepare_snrna_subset.py` (those two columns slipped into
  the student file because the strip-list used the README's casing). Fixed in
  `src/gbmspace_utils/data.py::SNRNA_ANSWER_KEY_OBS_COLUMNS`. **Lesson: verify strip-lists
  against actual column names, never trust documentation casing.**
- Visium `anndata_selected/*.h5ad` files have ~10 duplicate gene symbols (multi-mapped
  Ensembl IDs, e.g. `TBCE`, `MATR3`) — handled with `var_names_make_unique()` in
  `scripts/02_prepare_visium_subset.py`.
- The paper's own Methods text and figure legends disagree in a few places — worth telling
  students about rather than silently picking one (good "real papers are imperfect"
  teaching moments):
  - Cluster-level malignant-call threshold: ≥3% (Methods text) vs. ≥5% (Ext. Data Fig. 3C/3E legend).
  - cell2fate QC thresholds: max latent time >20 / transition score >0.25 (Methods) vs. >25 / >0.2 (Ext. Data Fig. 17A legend).
  - Visium spot count: 338,481 (Results text) vs. 377,149 (Table S2 total) — likely post-QC vs. raw.

## Paper-faithful parameters reference (for whoever writes/audits notebook content)

- **snRNA QC** (nuclei): genes<500 removed, UMI<1000 removed, mito%>10 removed; Scrublet
  doublets + 2-step MAD filtering (FDR<0.05 cell-level, FDR<0.1 cluster-level); UMI>75,000
  removed post-doublet-calling.
- **Integration**: paper used scVI only (50 latent dims, 2 hidden layers, 1024 nodes/layer;
  batch key = 10x reaction; covariates = tumour ID, site, reaction date, cell-cycle phase).
  We additionally teach Harmony for comparison (paper didn't use it) — pedagogical choice,
  not a paper-fidelity one.
- **Malignant/TME split**: inferCNVpy, window=250 genes, reference = marker-clear TME
  clusters; CNA signal>0.02 AND CNA correlation>0.3 at cell level (see discrepancy above
  for the cluster-level threshold).
- **Malignant axis scoring**: `sc.tl.score_genes` per state (this is literally the paper's
  own method — see `src/gbmspace_utils/analysis.py::MALIGNANT_AXIS_MARKERS` for the exact
  gene sets used, transcribed from Methods/Table S5/S6), cross-checked in the paper via
  scPoli reference mapping (Braun et al. 2023 atlas) and decoupleR/MSigDB enrichment — we
  don't reproduce those two cross-checks, score_genes alone is the teaching-appropriate cut.
- **cell2location**: reference signature — max_epochs=400, batch_size=10000, lr=0.002,
  one reference per tumour. Spatial mapping — N_cells_per_location=30, detection_alpha=200,
  max_epochs=6000, batch_size≈25% of spots. See `scripts/03_benchmark_cell2location.py` for
  the CPU-timing-informed FAST preset used in the Level 2 notebook.
- **Niche analysis**: sklearn NMF, 16 factors/tumour in the paper (cross-tumour cohort);
  we scale down given far fewer spots in 1-2 sections — let students try a few factor counts.
- **Spatial proximity network**: pairwise minimum spot distance via k-d tree, 25th
  percentile summary (implemented as `gbmspace_utils.analysis.spatial_proximity_network`).
- **Spatial intermixing**: Shannon entropy of per-spot cell2location abundance vector.

## Explicitly out of scope (with rationale)

- **spaceTree**: needs a from-scratch clone-calling pipeline (infercnvpy + epiAneufinder on
  paired snATAC-seq, which we don't have students build) before the GNN is even
  applicable, plus a 1920-point hyperparameter grid search just to get the paper's own
  defaults, and no real ground truth to validate against in a classroom setting.
  Independent assessment (not just deferring to the instructor's hunch) confirmed this is
  reasonably out of scope. A cheap substitute (overlay infercnvpy-derived clone clusters
  on top of the already-built cell2location map, purely descriptive) is mentioned as a
  1-paragraph "further reading" pointer in Level 2, not built as an exercise.
- **cell2fate**: needs spliced/unspliced counts generated via STARsolo from raw FASTQs —
  not derivable from the processed h5ad files we have. Revisit if/when that data arrives.

## Environment

`single_cell` conda env (`/shared/projects/tp_2630_ubordeaux_neuromics_184418/envs/single_cell`)
is shared across several course groups (informally the deployed version of the planned
`neuromics-sc` env) and was mid-build when this project started — missing several packages
from the official `cluster_setup/neuromics-sc.yml` wishlist. Added for this project specifically:
`squidpy`, `celltypist`, `harmonypy`, `decoupler` (all via plain `pip install`, no version
pins needed — confirmed no breakage of the existing scanpy/anndata/cell2location/scvi-tools/
torch stack after each addition). `infercnvpy` added during Level 1 build if not already
present (check the actual install log / `pip list` if auditing later). Did NOT install the
rest of the official wishlist (jax, xgboost, snakemake, cooler, etc.) — those serve other
course groups' projects, not this one. Jupyter kernel registered as "Python (single_cell)".
