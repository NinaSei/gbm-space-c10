# Decoding the Glioblastoma Microenvironment: From Single Cells to Spatial Architecture

## CAJAL Neuromics 2026 — Computational Mini-Project (C10)

### Background

Glioblastoma (GBM) is the most aggressive primary brain tumor in adults. A defining
feature of GBM is its extreme cellular heterogeneity: tumors contain malignant cells in
diverse transcriptional states, embedded in a tumor microenvironment (TME) made up of
resident brain cells (microglia, astrocytes, oligodendrocytes, neurons) and infiltrating
immune cells (macrophages, T cells, and others). Malignant cells themselves are not one
thing — they span a range of states that resemble different stages of normal brain
development, plus stress/hypoxia-associated states, and these states are not randomly
distributed: they form a spatial and likely temporal trajectory across the tumor.

Single-nucleus RNA sequencing (snRNA-seq) captures the transcriptome of individual nuclei,
enabling unbiased discovery of cell types and states. Spatial transcriptomics technologies
like 10x Genomics Visium map gene expression onto intact tissue sections, preserving the
spatial context that dissociation-based methods lose — at the cost of each measurement
("spot") capturing a mixture of several cells rather than one. Together, these modalities
let us ask not just "what cell types are here?" but "how are they organized in space, and
what does that organization tell us about how the tumor grows?"

### The Dataset

You will analyze real **human glioblastoma** snRNA-seq and Visium spatial transcriptomics
data from multiple tumors, each sampled at several anatomical sites. For Level 1 you will
work with a subset of the snRNA-seq data; for Level 2, matched Visium sections from the
same tumors.

**Important:** For Level 1, you will NOT be told which paper this data comes from, or
what its published conclusions are. The goal is for you to discover the structure in the
data through your own analysis — clustering, marker genes, your own reasoning — not by
reading someone else's interpretation first. Please resist the temptation to search for
the dataset online. In Level 2, the source paper will be revealed, and you'll compare
your own results against the published findings.

### Project Overview

#### Level 1 — Cellular Census (Estimated: 2 days)
*"What cell types and cell states are present in the GBM tumor and its microenvironment?"*

You will learn the foundations of single-cell transcriptomics analysis:
- Loading and exploring snRNA-seq data (AnnData format)
- Quality control and preprocessing
- Batch correction / data integration across tumors (you'll try two different methods and
  compare them)
- Dimensionality reduction (PCA, UMAP) and unsupervised clustering
- Cell type annotation using marker genes and automated annotation tools
- Distinguishing malignant cells from the surrounding microenvironment
- Characterizing the malignant cell-state landscape and basic differential expression

By the end, you will have a full map of the cell populations in these tumors, and a
first look at how malignant cell states vary.

#### Level 2 — Spatial Context (Estimated: 2.5 days)
*"How are cell types and states organized in space?"*

You will learn spatial transcriptomics analysis, and the source paper will be revealed:
- Loading and exploring Visium spatial data
- Spatial visualization and quality control
- Mapping your Level 1 cell types onto tissue using **cell2location**
- Spatial niche / tissue-domain identification
- Spatial neighborhood and proximity analysis (which cell types/states sit near which?)
- Reproducing and critically evaluating specific published figures

#### Level 3 — not yet available
A third module using Xenium (single-cell-resolution spatial) data is planned for a future
iteration of this course once that data is ready. Not part of this project for now.

### Technical Setup

**Language:** Python, with the standard scverse stack.

**Key libraries:** `scanpy`, `squidpy`, `anndata`, `cell2location`, `scvi-tools`,
`harmonypy`, `celltypist`, `matplotlib`/`seaborn`, `numpy`/`pandas`/`scipy`.

**Computing environment:** the shared `single_cell` conda environment (`conda activate
single_cell`) has everything pre-installed; launch with `jupyter lab`.

**AI assistance:** you have access to Claude/ChatGPT for coding help. Use AI tools as a
learning accelerator, not a replacement for understanding — if a suggested function or
parameter is unfamiliar, take a moment to learn what it does before using it.

### Tips for Success

- **Plot early, plot often.** Visualization is your best tool for understanding data.
- **Check intermediate results.** Print shapes, `.head()`, summary statistics. Trust but verify.
- **Justify your choices from the data you're looking at**, not from a remembered rule of
  thumb — a QC threshold or cluster resolution should be defensible from your own plots.
- **Ask "why" at every step.** Why normalize this way? Why these thresholds? Why does
  this cluster look like this? Understanding the reasoning is what transfers to your own
  future projects.
- **Document your reasoning** in markdown cells as you go — this is how real analysis works.
- It's fine — expected, even — for your results to differ somewhat from a classmate's.
  Different reasonable choices lead to different reasonable answers.

### Notation and Conventions

- 🔬 **TASK:** an analysis step for you to complete. Read the instructions carefully.
- 💡 **HINT:** a pointer if you're stuck.
- ❓ **QUESTION:** a conceptual question to think about and discuss — no code needed.
- ⚠️ **CHECKPOINT:** a rough expected range to sanity-check your own results against. If
  you're far outside the range, something upstream is worth revisiting — it doesn't mean
  there's exactly one right answer.

### Getting Started

1. **Environment:** `conda activate single_cell`, then `jupyter lab`.
2. **Data:** already prepared for you as `.h5ad` files — paths are given in each notebook.
3. **Notebooks:** open `notebooks/level1/01_snrna_analysis_student.ipynb` to begin.

### References

For Level 1, you should rely on:
- The [scanpy documentation](https://scanpy.readthedocs.io/)
- The [Single-cell best practices book](https://www.sc-best-practices.org/)
- Your instructors and fellow students

Further references (cell2location, squidpy spatial tutorials) will be pointed out as you
reach Level 2.
