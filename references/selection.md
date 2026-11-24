# GEO cohort selection and scoring

## Verify eligibility

Record the main purpose (an atlas, a condition comparison, or the higher priority if both apply), tissue, species, sampling site, and target cell types. For comparisons, define the target and reference conditions, independent replicate, and pairing. Verify each accession on its GEO Series page, then check the relevant Sample records, supplementary files, and linked author repositories. Record the official link, access date, and source for each material claim. Leave unpublished counts unknown.

For this multi-sample shortlist, require at least two distinguishable biological samples and an accessible cell-level expression matrix. Count donors, biological samples, libraries, and called cells separately. Technical repeats do not add independent samples. Preserve pairing between samples from the same donor. If only FASTQ files remain after checking linked deposits, mark the cohort **awaiting quantification**. For a dataset the user has already selected, assess feasibility for its intended use.

## Score cohorts for their intended use

For a **condition comparison**, score each independent cohort, contrast, and target cell type on a 10-point scale. Flag uncertain cell-type coverage for verification after import.

| Criterion | Points | Scoring guide |
|---|---:|---|
| Question and tissue match | 0–2 | Give 2 for a match on disease or treatment, comparator, and sampling site, 1 for a partial match, and 0 for a critical mismatch. |
| Effective independent replication | 0–3 | Use the smaller group's eligible donor count or the number of complete pairs. Award 0 for one or fewer, 1 for two, 2 for three to five, and 3 for six or more. Prefer at least three independent donors per group for case-control studies. |
| Target cell coverage | 0–2 | Give 2 when most donors in both groups contribute enough target cells, 1 for uneven but usable coverage, and 0 when a few donors dominate. |
| Confounding | 0–2 | Give 2 when condition is distinguishable from batch and key covariates can be addressed, 1 for substantial residual confounding, and 0 for complete confounding. Limit that contrast to description when fully confounded. |
| QC and cell identity | 0–1 | Give 1 when per-sample QC is reviewable and identity can be checked against author labels, markers, or a suitable reference. |

For an **atlas**, score five criteria independently from 0 to 2: biological question and tissue match, coverage of relevant tissues or states across samples, interpretability of the expression matrix and its scale, traceability of cells to samples and batches, and evidence supporting cell identity. Award 2 for sufficient evidence, 1 for partial fulfillment, and 0 for a verified failure. Single-condition studies can qualify.

State the evidence for every score. If a critical fact is unknown or a score range spans tiers, report the range and mark the candidate **pending verification**. For a feasible use with verified inputs, classify 8–10 as high priority, 5–7 as an option, and 0–4 as low priority. Verify raw gene counts for pseudobulk expression. Document the specific inference affected by confounding, missing replicates, or missing inputs.

## Deliver the shortlist

Write `dataset_candidates.xlsx` in the working directory with separate sheets for candidate evidence, scores by purpose, and final selections. Include database, accession and linked cohorts, title, official link and access date, species, tissue, disease or treatment, scRNA-seq or snRNA-seq, assay platform, conditions, sample and donor counts, effective replicates per group, cell count, file format, raw-count availability, sample and cell metadata, author annotations, download route, integration feasibility, risks, and recommendation. Distinguish unfiltered droplet barcodes from called cells.

Group by priority use and verification status, then rank within a use by score and donor coverage. Retain up to five independent cohorts in total. Track duplicate accessions and multiple uses of one GSE under a single shortlist entry. Before examining outcomes for replication, designate discovery and validation cohorts and check for reused samples or donors.
