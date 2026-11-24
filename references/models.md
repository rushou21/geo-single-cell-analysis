# Expression programs, reference mapping and virtual perturbations

Choose the method by the question, expression layer, biological replicates and available reference or model assets. Reuse verified results with matching inputs, versions and parameters.

| Question | Inputs and analysis | Evidence to return |
|---|---|---|
| What cells or states are present? | Use matched labeled references for annotation or retrieval. Use nonnegative expression counts for de novo program discovery. | Marker evidence, reference agreement and uncertainty, or program weights, stability and donor coverage. |
| What changed after an actual intervention? | Check measured treatment or guide assignment, baseline or non-targeting controls, biological replication, time and pairing. Analyze observed expression and composition using the [donor-level design](downstream.md). | Measured effect, unit of inference and uncertainty. |
| What might happen if expression changed? | With observational counts and an expressed candidate, evaluate a network-based virtual knockout. With compatible checkpoint, vocabulary and inputs, a model can simulate deletion or expression-rank changes. | A model-specific predicted response, controls and donor sensitivity. Biological follow-up requires independent evidence. |

Clarify the target of an ambiguous perturbation from context. A gene, a transcriptional program, a model representation and an organism-level phenotype require different readouts. Name any working interpretation and which endpoint the available data can measure.

## Prepare inputs and plan validation

- Preserve the main analysis object. Record the expression layer, matrix orientation, species, gene identifiers, mapping coverage and cell IDs for each export. When converting Seurat to AnnData, verify the transposed dimensions, identifiers and per-cell library totals wherever counts are available.
- Install the branches you will use. Use separate Python environments when packages require different PyTorch or CUDA builds. Record software, checkpoint and reference versions, seeds, compute resources and scripts. Update `results/analysis_index.csv` with output paths or the reason a branch could not run.
- When evaluating generalization, split by donor before tuning, selecting genes or defining target states. Keep all cells and libraries from a donor together. Check overlap with both the search reference and the pretraining corpus. Mark unverifiable overlap as unknown. Report within-cohort stability, independent-cohort replication, model predictions and measured interventions separately.

## Design a virtual perturbation

1. Specify the baseline population and donors, target genes, direction and magnitude of the simulated change, model and primary readout before inspecting predictions. For a partial knockdown or dose response, verify that the model implements the requested reduction and propagates it to the endpoint. Token deletion and network-node knockout model complete loss. Record any complete-loss sensitivity as a separate simulation and identify the limitation on the requested dose. Score a matched unchanged baseline for each modeled dose. If disease states are compared, fit or evaluate each state with sufficient donor coverage. Summarize candidate detection per donor and verify that the target survives feature selection or tokenization.
2. Choose an interpretable endpoint such as the rank of responding genes, a prespecified program response or distance to a frozen reference state. For a program containing the perturbed gene, also compute the response with that gene excluded. Use expression- and detection-matched control genes and an unchanged-input comparison when the model supports it. A knockout of a network node and a change in a token rank estimate different quantities.
3. Run each eligible single-target perturbation and its controls. Save the model inputs or their reconstruction recipe, retained features, donor and cell selections, baseline, control identities, raw predictions and summaries. For an ineligible target, record the missing prerequisite and continue with other targets or compatible methods.
4. Repeat across donor splits or donor-level resamples where replication permits. Report the variation and its source, the control distribution and the tested family if reporting adjusted significance. A model score quantifies a prediction. Distinguish a measurable predicted shift, an unstable estimate, a target with no modeled connections and a target the model cannot evaluate. An unmeasured phenotype or causal treatment effect remains unidentified from observational RNA alone.

## scGPT for annotation review

**Setup.** Install the Python package with `python -m pip install scgpt` in an environment compatible with the selected release. Download a checkpoint with its vocabulary and model configuration. Obtain a labeled reference matched to tissue, species and label resolution. The reference-mapping tutorial supports CPU embeddings with the fast transformer disabled. Faiss is optional for small custom references and required to query the published Faiss atlas index. [Installation and model zoo](https://github.com/bowang-lab/scGPT) · [Reference mapping tutorial](https://scgpt.readthedocs.io/en/stable/tutorial_reference_mapping.html)

Embed reference and query cells with the same checkpoint and preprocessing. Use reference neighbors to propose labels. Compare predictions against Seurat label transfer or SingleR using the same reference and held-out donors. With independently verified labels, report macro F1, per-type recall and the fraction left unassigned. Otherwise report agreement, conflicts and marker evidence. Submit per-cell predictions, vocabulary coverage and evaluation tables from `results/scGPT/` with the annotation review.

## SCimilarity for cross-study cell search

**Setup.** Install the Python package with `python -m pip install scimilarity`. Download and unpack the reference bundle for `CellQuery`, including encoder weights, the ordered gene list, the search index and indexed cell metadata. Check the available disk space for the chosen bundle. [Package and downloads](https://github.com/Genentech/scimilarity) · [Reference bundle](https://zenodo.org/records/10685499) · [Cell search tutorial](https://genentech.github.io/scimilarity/notebooks/cell_search_tutorial_1.html)

Start with verified human RNA counts, align gene symbols to the model's gene order, scale counts to 10,000 per cell, then apply log1p. Record gene coverage. Save neighbor distances, candidate identities, tissues, source studies, available donor IDs and supporting or contradictory markers to `results/SCimilarity/`. Flag hits from the same GSE, duplicate deposits and shared donors. Cross-study matches nominate states to test in independent donors.

## cNMF for expression programs

**Setup.** Install the Python package with `python -m pip install cnmf`. The standard factorization runs on CPUs and learns programs from the supplied data. Its optional batch-correction preprocessing also uses `harmonypy` and `scikit-misc`. [Installation and workflow](https://github.com/dylkot/cNMF)

Start with a nonnegative, post-QC cells-by-genes count matrix and let the workflow select features from the full gene set. Fit within lineages to resolve states. A cross-lineage question can justify a whole-cohort fit. Compare program counts (`K`) and random initializations using consensus stability, reconstruction error and gene content. Save program weights, representative genes, per-cell usage and donor-level summaries in `results/cNMF/`. Check for associations with depth, stress, cell cycle or a single donor. For replication, freeze discovery programs and project held-out donors onto them.

## Geneformer for in silico perturbation

**Setup.** The authors distribute the Python package `geneformer` and model files through Hugging Face. Install Git LFS, clone the official repository and run `python -m pip install .` inside that checkout. Select a human checkpoint appropriate to the tissue and disease context. Match its tokenizer, token dictionary and gene-normalization resources to the checkpoint generation. Plan a compatible GPU environment for efficient perturbation inference. [Installation and checkpoints](https://huggingface.co/ctheodoris/Geneformer) · [Tokenizer](https://geneformer.readthedocs.io/en/latest/geneformer.tokenizer.html) · [Perturber](https://geneformer.readthedocs.io/en/latest/geneformer.in_silico_perturber.html)

Within one cell type, specify candidate genes, a source state and, when justified, a target state. Tokenize post-QC, full-gene raw counts with matching Ensembl IDs and per-cell `n_counts`. Record sequence truncation and how many cells and donors actually contain each candidate token. Verify the installed version's settings for grouped perturbations and submit one candidate per call for individual tests.

Model deletion by removing a gene token and overexpression by promoting its rank. Include controls matched on expression, detection or rank. Report embedding shifts, coverage and donor-level consistency in `results/Geneformer/`. Interpret direction toward a target only when a target reference was fixed in advance. Otherwise report the size of the general shift. Independent intervention data are needed to test the biological effect.

## scTenifoldKnk for network-based virtual knockout

**Setup.** Install the R package from CRAN with `install.packages("scTenifoldKnk")`. For an explicitly selected development revision, the authors also provide a GitHub installation route. The method learns a network from the supplied baseline cells. [Package and method](https://github.com/cailab-tamu/scTenifoldKnk)

Use a genes-by-cells count matrix from adequately sampled, unperturbed cells of the target type. Check that each candidate is expressed and enters the fitted network. Run individual virtual knockouts, then save differential-regulation rankings, pathway results and the set of genes tested in `results/scTenifoldKnk/`. Use donor resampling or donor-specific networks to assess stability and add control genes of comparable coverage. Interpret unsigned scores as magnitudes. If the installed version also estimates direction, label it as predicted and record the settings. Agreement with Geneformer on the same cohort is exploratory evidence.
