# Donor-level analysis after annotation

When starting from an annotated object, read the object, cell-level labels, sample table and available QC and annotation decisions. Verify that their versions and scope match the request. The standard project object is `clean_data/<GSE>_annotated.rds`. For external objects, preserve traceable original labels and document what can be verified. Run the requested branches, or assess each branch below for a full workflow.

## Study design and coverage

- For each contrast, record the target and reference groups, target cell types, independent biological unit, technical replicates, pairing, repeated measurements and planned covariates. Define the direction of comparison before reviewing test results. Label exploratory contrasts. In file names, use `<P>` for `<GSE>_<contrast_id>`, or `<GSE>_atlas` for atlas-only work. Use a unique short identifier `<CT>` for each cell type and retain the label mapping.
- Verify `cell_id`, `sample`, `donor`, `condition`, `batch` and `celltype`. Save the design in `clean_data/<P>_sample_info.csv`. In `results/design/<P>_coverage.csv`, record traceable pre- and post-QC cell counts per sample and type, total RNA counts when available, independent donors per group and complete pairs. Before testing, choose coverage and replication criteria appropriate to the assay and design. Check for systematic loss of a group or donor.
- Check estimability separately for each contrast and type. Report descriptive results for a contrast completely confounded with batch. Samples with uncertain independence can contribute to an atlas. Reassess eligibility for inference within the subset of verified independent units. Report cells as coverage and donors, animals or independent cultures as biological replicates.

## Composition and differential abundance

1. Reliable cell labels and sample assignments are sufficient to estimate composition. Define the denominator, such as all QC-passing cells, enriched cells or a parent population. Document how `Uncertain` and `doublet_flag` affect it. Record zero for an unobserved type in an eligible sample. Mark a proportion as missing when its sample is missing or its denominator is zero.
2. In `results/composition/`, save `<P>_sample_celltype_counts.csv`, `<P>_sample_celltype_proportions.csv`, per-sample stacked proportion plots and donor-level dot plots. Connect observations from the same donor in paired designs. Use sample-level type counts and denominators in models that account for composition, pairing and repeated measurement. Consider miloR neighborhood differential abundance for continuous cell states when a comparable graph spans the samples and independent replication supports the comparison.
3. Save `<P>_differential_abundance.csv` in the same directory. Report effect direction, denominator or reference population, model and multiple-testing correction scope. Interpret changes in relative abundance in the context of sampling and enrichment. If a contrast cannot be estimated, retain the sample-level observations.

## Pseudobulk differential expression within cell types

1. Sum unnormalized RNA gene counts across cells within each biological sample, condition and cell type. Combine verified technical replicates of a sample. Keep distinct conditions, times and sites from one donor identifiable. If a sample has zero cells of a type, its composition count is zero and it contributes no expression library for that type. Match each pseudobulk column to its sample-table row in order.
2. Filter low-expression genes within each type. Check library sizes, sample PCA, outliers, retained donors per group, complete pairs and design matrix rank. Use edgeR quasi-likelihood tests or DESeq2 where counts and design support them. Complete two-condition donor pairs may use `~ donor + condition`. Choose a model appropriate to more complex repeated sampling. With normalized RNA alone, assess composition, eligible pathway scores and descriptive gene expression.
3. In `results/DEG/`, save each type's count matrix, sample table, `<P>_<CT>_DEG_all.csv` and `<P>_<CT>_DEG_significant.csv`. Retain column headers if the significant table has no rows. Report stable gene ID, symbol, target-versus-reference log2 fold change, statistic, raw P value, Benjamini-Hochberg adjusted P value and effective donor counts. Prespecify effect and significance thresholds and the family of tests for each correction. Plot donor-level expression. To compare response magnitude across types, use a cell-type-by-condition interaction or equivalent test that accounts for measurements from the same donor.

## Gene expression with normalized RNA only

For specified genes, summarize interpretable normalized expression by donor and cell type. Plot donor points and connect paired observations. Record the original transformation, summary scale and contributing cell count. Describe differences between group means on that scale. If a count-based DEG table is requested, check for original gene counts that can be aligned to the current cell IDs.

## Pathways and gene sets

- **GO or KEGG overrepresentation.** Within each type, test significant upregulated and downregulated genes separately. The background comprises genes tested in that contrast and mappable to that database. Save full results, foreground and background sizes, species, ID mapping and database version in `results/Enrich/`.
- **Preranked GSEA.** Save the directional ranks of all tested, mappable genes and the results by type in `results/GSEA/`. Use finite signed statistics, such as the Wald statistic or `sign(log2FC) * sqrt(F)` for a one-degree-of-freedom edgeR quasi-likelihood test. Document duplicate-ID and tie handling. Report the normalized enrichment score, adjusted P value and leading-edge genes. A valid ranking supports GSEA even when no genes pass the DEG significance threshold.
- **Cell-level scores.** Score prespecified gene sets when the expression scale fits the method and the measured genes provide adequate coverage. Summarize by type and sample. Compare scores using donors or the paired design. Distinguish an unavailable ranking, a tested result with no significant change and a supported direction of change.

## Additional analyses with specific input requirements

| Branch | Required evidence, analysis and output |
|---|---|
| Pseudotime | For a continuous lineage with a biologically supported starting state, infer relative order with Slingshot or a comparable method. Check sensitivity to root selection and donor dominance. Save cell order, branches and gene trends in `results/trajectory/`. |
| RNA velocity | Use cell-matched spliced and unspliced counts when the process fits the kinetic model. Inspect representative gene phase portraits and model fits. Save velocity estimates in `results/velocity/`. |
| Lineage tracing | Verify heritable lineage labels, their assignment to cells and reconstruction consistency. Save lineage trees in `results/lineage/`. |
| Gene regulatory networks | When gene and transcription-factor coverage and species-specific motif resources support the method, run SCENIC or another appropriate approach. Save candidate regulons, supporting evidence and sample-level activity summaries in `results/GRN/`. |
| Cell communication | Check cell labels, RNA scale, species-matched ligand-receptor resources and coverage of both sender and receiver types within donors. Save candidate cell pairs and signaling axes in `results/communication/`. For condition comparisons, assess variation across donors and sensitivity to cell counts. Interpret inferred interactions as hypotheses. |
| Measured perturbations | Use observed treatments, controls and biological replicates to assess within-type expression or state changes. Verify cell-level perturbation assignments when required. Save effects and donor coverage in `results/perturbation/`. |
| Deconvolution of an existing bulk cohort | Where a bulk cohort exists and the single-cell reference represents its tissue and cell types, check species, gene IDs and expression scales. Save sample composition estimates, difficult-to-distinguish types and available independent measurements for comparison in `results/deconvolution/`. |

## Deliverables and verification

Maintain one `results/analysis_index.csv` per GSE. Record the branch, contrast, type, required inputs, verified evidence, effective donors and status. Use `Completed`, `Completed without significant findings`, `Descriptive only`, `Insufficient input or design` or `Failed`. Link completed entries to files that open. For restricted or failed branches, list sources checked and the specific limitation or error. Continue eligible analyses when another branch lacks input.

Save executed scripts in `scripts/`. Record software, model and resource versions, thresholds and random seeds. Deliver tables, PDFs and high-resolution PNGs. Write the English report to `report/<P>_single_cell_analysis_report.md`. For each research question, report the donor count, effect size, uncertainty and scope of interpretation. With sufficient replication, check sensitivity to omitting one donor at a time or changing coverage thresholds. Before external replication, verify that donors and cohorts are independent and that tissue and contrast direction align. Evaluate the types, programs or candidate genes fixed in the discovery analysis.
