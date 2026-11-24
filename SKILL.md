---
name: geo-single-cell-analysis
description: Select GEO scRNA-seq or snRNA-seq cohorts, run a complete multi-sample analysis from expression counts, resume from a verified object, or review a single-cell workflow. Covers cell identity, donor-level inference, trajectories, expression programs and computational perturbations.
---

# Single-Cell RNA-seq Analysis

## Match the requested scope

- **Selection or review.** For cohort selection, deliver the verified shortlist. For workflow review, evaluate the design and evidence. Follow any stopping point in the request.
- **Full analysis.** Open the [execution and acceptance guide](references/full-workflow.md) first. Start with the earliest available in-scope input, run the core analysis, and evaluate each conditional branch against the biological question. Preserve authors’ labels and coordinates as comparators. A published atlas or a finished donor-level model alone does not establish that QC, clustering and annotation were performed in this run.
- **Targeted analysis or resume.** Follow the requested entry point. Inspect the object’s count/normalized layers, cell IDs, sample manifest, labels and processing history. Reuse a scientifically suitable checkpoint with matching inputs and scope. Recompute from the earliest affected stage when these change.
- **Skill maintenance.** If the request is to improve this skill, change the reusable instructions or tools and validate them using isolated examples. Running or resuming a biological project requires a project-analysis request. Honor a subsequent pause immediately.

## Find the method

| Stage | Guide |
|---|---|
| Check the local runtime, memory and packages for a chosen analysis | [Environment and packages](references/environment.md) |
| Select and score public cohorts for an atlas or a comparison | [GEO selection and scoring](references/selection.md) |
| Inspect input layers, map libraries and donors, review QC, normalize, build graphs, cluster and annotate | [Preprocessing and annotation](references/preprocessing.md) |
| Analyze composition, differential expression, pathways, trajectories, regulation, communication or measured interventions | [Donor-level analysis](references/downstream.md) |
| Discover expression programs, assess reference mappings or simulate gene perturbations | [Programs and models](references/models.md) |

## Decisions that carry across stages

Specify species, tissue, assay, independent unit, comparator, pairing and target population. Track cells, captures, samples and donors separately. Check estimability, cell coverage and donor overlap before making disease, treatment or replication claims. Analyze independent cohorts separately by default. Count models use unnormalized counts. Preserve original matrices and annotations, including their limitations.

Respect the user’s chosen review mode. In an interactive run, present sample-specific QC impact and the proposed annotation map at the requested checkpoints. Explicit delegation of routine scientific decisions authorizes making and recording these decisions without asking again. A quiet run suppresses routine updates. Changes to the biological objective, destructive modifications and genuinely missing information follow the usual authorization rules.

## Project outputs

Save a requested screening workbook in the working directory. Start each study under `<GSE>_GEO_single-cell_analysis_project/` with `raw_data/`, `clean_data/`, `scripts/`, `results/` and `report/`. A stable cohort ID can replace a GEO accession. Keep per-sample QC in `results/QC/`. In existing projects preserve prior versions and reuse verified outputs where appropriate. Write reproducible scripts, numeric tables, figures and a report in the requested language (English by default). For full runs, verify the study’s analysis index and the numerical results before describing the workflow as complete.
