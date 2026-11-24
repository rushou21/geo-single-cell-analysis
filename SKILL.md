---
name: geo-single-cell-analysis
description: Select and score GEO single-cell and single-nucleus RNA-seq cohorts, or continue from an expression matrix, Seurat object, or AnnData object. Use for multi-sample QC, clustering, annotation, donor-level comparisons, expression programs, and review of these workflows.
---

# Single-Cell RNA-seq Analysis

Start at the stage the user requested. For a supplied accession, verify the study and its files. For an existing object, inspect the RNA layers, cell metadata, and processing history. For a workflow review, deliver findings about the design. When a full analysis is requested, run each branch that the data and design support.

## Choose a starting point

| Task | Guide |
|---|---|
| Set up a project, identify the packages needed for a stage, or check the local runtime | [Environment and packages](references/environment.md) |
| Find public cohorts and rank them for an atlas or a case-control comparison | [GEO selection and scoring](references/selection.md) |
| Download a matrix, align cells to samples, review QC, cluster, find markers, or finalize labels | [Preprocessing and annotation](references/preprocessing.md) |
| Compare composition or expression across donors, test pathways, or assess trajectories and other conditional analyses | [Donor-level analysis](references/downstream.md) |
| Discover expression programs, search reference atlases, evaluate model-assisted labels, or simulate a perturbation | [Programs and models](references/models.md) |

## Decide which analyses the data support

1. Establish the species, tissue, assay, biological question, and independent sampling unit. Map cells to libraries, samples, and donors. Before a group comparison, define the contrast, reference group, pairing, and target cell types. Check donor and cell coverage separately for each type.
2. Verify what each RNA layer contains. Use raw gene counts for count models. Use normalized RNA for compatible expression summaries. Published labels and coordinates can still support atlas displays, and labels matched to samples can support composition estimates. For FASTQ-only records, check the authors' repositories for a cell-level matrix and flag outstanding quantification.
3. Preserve the downloaded data and a pre-QC object. In a full workflow, show the expected per-sample impact and obtain approval of that cohort's QC plan before filtering. Submit the proposed annotation map for approval before writing the final `celltype` field. Reuse matching approvals and outputs when resuming. If the user supplies finalized labels or explicitly selects existing labels for downstream analysis, record their source, scope, and QC history, then proceed from that stage.
4. Analyze independent cohorts separately by default. Use donors, animals, or another verified independent unit for inference. If batch is fully confounded with condition, describe the affected contrast and continue other estimable analyses. Check study and donor overlap before calling another cohort an independent replication.

## Save and report

Save the screening workbook in the working directory. Start each new GEO study under `<GSE>_GEO_single-cell_analysis_project/` with `raw_data/`, `clean_data/`, `scripts/`, `results/`, and `report/`. For a local study without a GEO accession, substitute its stable cohort ID. In an existing project, reuse verified inputs and mappings. Put QC figures and tables in `results/QC/`.

For a full workflow, maintain one `results/analysis_index.csv` per study with branch, contrast, cell type, required inputs, supporting evidence, status, and output paths. Document why a branch was skipped and continue eligible work. Deliver reproducible scripts, tables, figures, and an English report by default. Give effect sizes, uncertainty, and the number of independent donors behind the findings. Identify within-cohort resampling, held-out donors, independent replication, and model predictions separately.
