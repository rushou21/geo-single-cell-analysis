# Download, quality control, clustering and cell annotation

Use a separate `<GSE>_GEO_single-cell_analysis_project/` directory for each selected cohort. Paths below are relative to that directory. When resuming an existing project, locate the inputs, versions and confirmed decisions before continuing from the requested stage.

## Download and identify the RNA expression layers

Create `raw_data/`, `clean_data/`, `scripts/`, `results/` and `report/`. Describe their contents in the project README in English. Use GEOquery for sample metadata when available. Inspect both GSE and GSM supplementary files and any repository linked by the authors. Download the matrix, feature and barcode tables, sample groups, cell metadata, author annotations and accompanying documentation. Keep original files by library under `raw_data/<GSE>/`. In that directory, write a `download_log.txt` with source, timestamp, size, path, status and any available checksums.

Verify the species, whether the experiment captured cells or nuclei, assay technology, matrix orientation and contents of each RNA layer. Inspect the 10x MTX matrix, features and barcodes, or the contents of the H5, H5AD, RDS or text matrix. Select Gene Expression features from multimodal inputs. Check values against the authors' processing description. A filtered 10x matrix can still contain raw UMI counts. In H5AD, establish the provenance of `.raw`, `X` and `layers["counts"]` individually. Report dimensions, barcode count, called cell or nucleus count, biological sample count and verified donor count.

| Verified input | Applicable work |
|---|---|
| Unnormalized gene counts | Preserve sparse counts for the full gene set. Compute QC metrics and use compatible normalization and donor-level count models. |
| Normalized RNA only | Record the transformation and author QC. Use the existing scale for compatible clustering, marker analysis or scoring. Mark analyses that require raw counts as missing input. |
| Scaled or integrated values, coordinates or author labels only | Carry forward verified coordinates, clusters, labels and author evidence. Summarize composition if cells map reliably to samples. Identify which results were recalculated and which came from the authors. |
| FASTQ only | Check repositories linked by the authors for a count matrix. If none is available, mark the cohort `Pending quantification` and continue with other cohorts in a batch search. |

Save the download script at `scripts/01_download_check_scRNA.R` and its verification report at `report/download_verification.md`.

## Construct the pre-QC object

- Preserve original feature IDs, version suffixes, gene symbols, species and reference build. Use a stable unique feature key. Use version-matched annotation to record duplicate symbols, one-to-many mappings and unmapped features.
- Write one row per biological sample in `clean_data/sample_manifest.csv`, with `sample`, `donor`, `condition`, `batch`, `tissue` and `technology`. In `clean_data/library_map.csv`, map `library_id` and `capture_id` to the actual samples. Pooled libraries can contain several donors. Assign cells to donors only when demultiplexing supports the assignment.
- Build `cell_id` from a unique library or source-matrix identifier and the original barcode. Check reused barcodes across libraries, resequencing of the same cells and unmatched records. Save traceable sample fields, original author clusters, cell labels and available QC fields in `clean_data/cell_metadata.csv`. Report cells of unknown donor separately.
- For unfiltered droplets, document the cell-calling method and barcode-level calls. Reconcile the number of input barcodes with the number of candidate cells or nuclei. Use called cells or nuclei as the QC denominator. Record any author filtering, retain all candidate cells at this stage and save `clean_data/<GSE>_preQC.rds`, `scripts/02_prepare_scRNA.R` and `report/input_and_mapping.md`.

## Review and approve the sample-level QC plan

1. From RNA counts, calculate `nCount_RNA`, `nFeature_RNA` and `percent.mt`. Check the species and feature mapping for mitochondrial genes. Record the mitochondrial fraction as missing if these genes cannot be identified. Plot each metric by sample and plot total counts against detected genes. Interpret potential thresholds in light of tissue, cell versus nucleus capture, and each sample's distribution. When counts are unavailable, review only QC information supported by the authors' records.
2. Assess doublets per independent capture and ambient RNA when compatible droplet data are available. Save per-cell risk flags. For each sample, report how many cells meet each candidate rule, the number that meet any rule after deduplication, and the expected counts and percentages removed and retained. Flag donors or lineages that would lose a disproportionate number of cells. If adopting the authors' QC, document why it fits this analysis.
3. Place plots, flags and sample summaries in `results/QC/`, and the script in `scripts/03_QC_review.R`. Write the accession, input object version, plan version, proposed rules and expected impact to `report/QC_review.md`. Show this plan to the user and obtain their confirmation for that version before filtering. Reuse an existing confirmation for the same version. If thresholds change, show the revised impact and obtain confirmation of the revised plan.
4. Apply the confirmed plan once to the matching pre-QC object, or retain the authors' QC as agreed. Preserve available raw counts, cell IDs and metadata. Record the decision and reason per cell. Reconcile actual and predicted retained counts per sample and identify which rules explain any discrepancies. Save per-sample objects in `clean_data/QC_filtered/` and observed outcomes in `results/QC/`. Reuse matching results on reruns. Rebuild from the pre-QC object when the plan changes.

## Integration, clustering and markers

With counts, choose LogNormalize or, for suitable UMI data, SCTransform. Use existing normalized RNA on its documented scale. When the data support a new embedding, retain unintegrated PCA, neighbor graph, UMAP and clusters. Color plots by sample, donor, condition and cluster. Consider RPCA, CCA or Harmony when a technical batch effect and shared populations support integration. Compare within-type mixing across batches, known markers, retention of biological states and dominance by individual donors. The unintegrated representation can be the primary result. Treat comparisons with complete condition-batch confounding as descriptive.

Build the neighbor graph and cluster in the selected space. Compare at least three appropriate resolutions and report population sizes, splits, merges, and sample, donor and condition composition. Check stability across seeds or resamples when claiming stable clusters. Find markers for final clusters on an interpretable normalized RNA layer. If Seurat v5 RNA layers remain split by sample, run `JoinLayers()` before marker testing. After SCTransform, derive a standard normalized RNA layer from retained RNA counts when needed. Export per-cluster marker tables with log2 fold change, detection fractions inside and outside the cluster, and applicable adjusted P values. Include a DotPlot, representative FeaturePlots and a heatmap of top markers.

Save `clean_data/<GSE>_clustered.rds`, `results/clustering/`, `results/markers/`, `scripts/04_integrate_cluster_markers.R` and `report/clustering_and_markers.md`. Verified author clusters, coordinates or labels can also serve as the entry point for annotation. Document their source and limitations.

## Review and approve the cell-type mapping

For each cluster, summarize tissue-appropriate supporting and conflicting markers, author labels, heterogeneity, donor representation, candidate cell type, alternatives and confidence. When only credible author cell-level labels are available, review mappings from those labels. For mixed-lineage marker signals, examine coexpression within the same cell, ambient RNA, mixed populations and capture-level doublet scores. Keep `doublet_flag` and `celltype` as separate fields. With a suitable reference, use SingleR or Seurat label transfer for comparison. For scGPT mapping or SCimilarity retrieval, see [Expression programs and models](models.md).

Write `results/annotation/annotation_review.csv` with the accession, mapping version, original cluster or author label, candidate label, evidence and unresolved issues. Include marker evidence plots and a candidate-label UMAP when available. Obtain the user's confirmation of that mapping version before assigning final labels. Record manual changes, preserve original clusters and author labels, and add `celltype`. Mark unconfirmed entries as `Uncertain`. Deliver the final mapping, `clean_data/<GSE>_annotated.rds`, per-cell metadata, counts and proportions by sample and type, available annotation plots, scripts and an English report.
