# Single-Cell RNA-seq Analysis

A Codex skill for multi-sample single-cell and single-nucleus RNA-seq studies. Screen GEO cohorts for a biological question, import a cell-level matrix, or continue from an annotated Seurat or AnnData object. The workflow keeps each donor's contribution visible from quality control through statistical inference.

## Install the skill

Run this command from the root of the research project where you want to use the skill. It places the entry point at `.agents/skills/geo-single-cell-analysis/SKILL.md`.

```sh
git clone https://github.com/rushou21/geo-single-cell-analysis.git .agents/skills/geo-single-cell-analysis
```

You can also download the repository ZIP and extract its contents at that same location. Open a Codex conversation in the project and invoke `$geo-single-cell-analysis`. Cloning installs the workflow instructions. Set up the software for the analysis stage you intend to run using the [environment and package guide](references/environment.md).

## What do I need?

| Task | Prerequisites |
|---|---|
| Review a study design or screen GEO | Codex with access to this project. GEO screening also needs network access to GEO and the linked data hosts. Record each accession and the evidence supporting inclusion. |
| Run the core R workflow | R with `Rscript`, a writable R package library, and storage for input matrices and derived objects. Seurat handles clustering and markers. GEOquery retrieves GEO metadata. Use BiocManager to match Bioconductor packages to the installed R release. |
| Compare conditions | Sample-to-donor and condition mappings, biological replication, and a design that separates the intended effect from batch. Cell composition uses sample-level type counts. Type-specific pseudobulk differential expression needs raw RNA gene counts and edgeR or DESeq2. |
| Run an extension | Choose packages and resources for that branch. For example, cNMF uses a separate Python environment, Geneformer needs compatible model weights and a tokenizer, and scTenifoldKnk runs in R. The [model guide](references/models.md) gives the inputs, software sources, and interpretation for each method. |

**Companion skills.** This repository is the only Codex skill required for the workflow. If already available in your installation, `bio-expression-matrix-counts-ingest` can help inspect a counts matrix, `bio-expression-matrix-metadata-joins` can help align sample labels, and `bio-differential-expression-edger-basics` can help fit an edgeR model to pseudobulk data. These names identify optional agent instructions. R and Python packages are installed separately.

## Example requests

> Use $geo-single-cell-analysis to find human kidney scRNA-seq cohorts with cases and controls. Verify independent donor counts, cell-level matrices, and author annotations. Rank cohorts for donor-level comparison and stop after the shortlist.

> Use $geo-single-cell-analysis on this annotated Seurat object. Check the RNA layers, pairing, and cell coverage. Compare cell-type proportions across donors and run pseudobulk differential expression for cell types with usable raw counts and replication.

## Workflow guides

| Guide | What it covers |
|---|---|
| [Environment and packages](references/environment.md) | Runtime requirements, package sources, installation commands, and checks before analysis. |
| [GEO selection and scoring](references/selection.md) | Verify official records, distinguish atlas and case-control uses, and deduplicate overlapping cohorts. |
| [Preprocessing and annotation](references/preprocessing.md) | Inspect counts and normalized layers, align metadata, review QC thresholds before filtering, and confirm cell-type labels. |
| [Donor-level analysis](references/downstream.md) | Estimate cell composition, test expression within types, and assess pathways, trajectories, regulatory networks, or communication when their inputs are available. |
| [Programs and models](references/models.md) | Discover programs with cNMF, check cell identities and states with scGPT or SCimilarity, and explore virtual perturbations with Geneformer or scTenifoldKnk. |

The [skill entry point](SKILL.md) explains how to resume partway through a study. Analysis outputs include reproducible scripts, tables, figures, and an English report. The workflow records the number of contributing donors and distinguishes descriptive findings, within-study inference, external replication, and model predictions.

## License

The skill and its documentation are available under the [MIT License](LICENSE). External software, datasets, reference atlases, and model weights are distributed under their respective terms.
