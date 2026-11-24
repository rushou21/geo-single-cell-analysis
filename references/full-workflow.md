# Executing and accepting a full single-cell workflow

## Establish the unit of work

For each study, record the biological question, assay, tissue, available input level, comparison, independent unit, candidate lineage or target genes, and whether the user requested new processing or selected an existing object. Record intended discovery and replication roles before looking at outcomes. In a multi-cohort study, a branch may be feasible in only one cohort.

Start `results/analysis_index.csv` from the [stage inventory](../assets/analysis_index_template.csv). It lists the core stages and conditional analyses, with the inputs that distinguish them. For a focused task, retain the requested stages and their dependencies. Expand a row if different contrasts, cell types or methods have different decisions. Add a row for a requested method beyond the inventory. Each row describes one independently decidable analysis. In an existing project, keep earlier records and migrate their columns in a copy when needed.

## Carry out the core analysis

1. **Design and inputs.** For public-data discovery, screen studies and independent donors. For a supplied object, verify the source and layer directly. Preserve cell/feature identifiers, counts, raw metadata, feature annotations and checksums. Identify the earliest recoverable step (FASTQ, droplet counts, called-cell counts, normalized matrix, or labels). Follow referenced data hosts when a necessary matrix or annotation is missing.
2. **QC and structure.** Save pre-filter metrics, per-sample thresholds and expected losses, then reconcile actual retained cells and donors. Use appropriate droplet, ambient RNA and doublet checks for the available input. Fit normalization, feature selection, PCA, a neighbor graph, embeddings and clusters on a suitable expression layer. Assess technical mixing and preservation of biology before choosing an integrated representation. Compare clustering resolutions and check representation across donors. An externally filtered or enriched source limits reconstruction of earlier steps and abundance denominators.
3. **Identity.** Compute cluster markers, examine positive and conflicting markers, compare to source labels or a reference, and retain uncertainty. If a specific lineage is the target, check separation from related types and resolve within-lineage states when coverage supports it. Avoid using the endpoint gene set as the sole definition of the cells that will be tested. Save the final count-bearing object, cell-level crosswalk and evidence for the labels.
4. **Inference.** Rebuild group counts and model matrices after QC and annotation. Fit the applicable composition, pseudobulk, pathway and program analyses with biological replicates. Give effect sizes, uncertainty, effective samples per group and the multiple-testing family. Keep descriptive marker tests distinct from condition contrasts. Run donor sensitivity analyses and external replication when available.
5. **Conditional analyses.** For each relevant branch, inspect its actual inputs and run a defensible method when supported. For a state-transition question, evaluate the manifold, root evidence and alternate roots. For a specified gene or program with a perturbation question, evaluate an appropriate virtual perturbation, target coverage, matched controls and held-out or resampled donors. A cross-sectional assay can support exploratory state ordering. A cohort without measured interventions may support a model prediction. Velocity needs spliced/unspliced layers and lineage tracing needs heritable labels. Assess regulatory networks, interaction partners, supervised mapping or bulk deconvolution on their own prerequisites. See the [donor-level](downstream.md) and [model](models.md) guides for acceptance evidence.
6. **Interpretation.** Reconcile the report’s sample counts and headline estimates to the saved tables. Trace each finding to the object, contrast and input version used. Identify where a result is descriptive, inferred within a cohort, externally replicated, experimentally measured or predicted in silico.

## Track what actually happened

The index columns are `stage_id,branch,contrast,cell_type,required_inputs,evidence,status,output_paths`. Paths are relative to the study directory. Separate multiple paths with a semicolon. Include additional columns for effective donors, versions or execution dates when helpful. Evidence should identify a checked artifact, layer, publication, diagnostic, exact missing input or scope decision. Use the applicable status below.

| Status | Interpretation and evidence |
|---|---|
| Pending | Work remains or a running job has yet to return. |
| Completed | The stage ran successfully. Link its scientific or processing outputs. |
| Completed without significant findings | The test ran. Link its estimates and uncertainty, including null findings. |
| Reused | Link a verified checkpoint or imported result and record its source, version, coverage and applicability. |
| Descriptive only | Link the actual descriptive output and identify the inference the design limits. |
| Not applicable | State the biological or scope reason. Reassess if a later request explicitly asks for the branch. |
| Insufficient input or design | Identify the missing input or failed design requirement and the sources, alternatives or diagnostics checked. |
| Failed | Record the error, recovery attempted and remaining blocker. Continue independent branches. |

## Verify delivery

Use [the index checker](../scripts/check_workflow.py) from any working directory, supplying its installed path where needed.

```text
python <skill-dir>/scripts/check_workflow.py init <study-directory>
python <skill-dir>/scripts/check_workflow.py check <study-directory> --full
python <skill-dir>/scripts/check_workflow.py check <study-directory> --fresh-counts
python <skill-dir>/scripts/check_workflow.py check <study-directory> --require-run pseudotime virtual_perturbation
```

Initialization preserves an existing index. The full check identifies unassessed stages, unfinished entries and missing output files. Use `--fresh-counts` when claiming an end-to-end run from counts with newly computed QC, normalization, graph, clusters and annotations. Use `--require-run` for named analyses whose results are reported as newly computed. These flags can be combined. If a branch has several rows with different outcomes, describe each outcome separately. A documented limitation or reused result can be appropriate to deliver and still fall short of a claim of new execution.

For a claim limited to a particular contrast or cell type, retain the full index and use `--index <project-relative-copy.csv>` to check the relevant rows with `--require-run`. Verify delivery of the full study against its original index.

Before closing a full run, inspect representative output files in their native formats, align matrix and metadata identifiers, reconcile QC totals and check the direction and uncertainty of reported effects. Inspect primary plots and the final report. For each explicitly requested analysis, name the result or the specific remaining limitation. A passing index check verifies bookkeeping and file presence. Scientific acceptance requires these content checks.
