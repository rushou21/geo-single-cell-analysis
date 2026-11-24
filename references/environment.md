# Environment and package setup

Choose the setup for the stage you plan to run. The skill itself is Markdown and YAML. Codex can use it to review a workflow as soon as the project contains `.agents/skills/geo-single-cell-analysis/SKILL.md`. No companion agent skill is required. GEO screening needs internet access to GEO and author-linked data hosts. R is needed when you execute the R workflow. Python is needed for selected readers, models and downstream methods.

## Prepare the project

- Use a supported R installation on Windows, macOS or Linux with `Rscript` on your path, a writable R library, and a project directory where the analysis can write files. Match the Bioconductor release to your R version. On Windows, use the matching Rtools when compiling packages with native code from source. On other systems, check the compiler and system libraries listed for the selected package. [Bioconductor installation](https://bioconductor.org/install/) · [Rtools by R version](https://cran.r-project.org/bin/windows/Rtools/)
- Estimate working space for the download, extracted matrices, pre-QC and final objects, and any reference index or checkpoint. Estimate memory from the matrix dimensions and any dense intermediate. Preserve sparse counts when reading and aggregating. Ordinary Seurat preprocessing can run on CPU. Check memory and accelerator support separately for each model.
- To inspect the local setup, run `Rscript --version` in a terminal. In R, run `sessionInfo()`, `.libPaths()` and, when available, `BiocManager::version()` and `BiocManager::valid()`. These checks do not install packages. The latter checks release consistency and may contact package repositories.

## Install the common R workflow

This example covers programmatic GEO access, a candidate workbook, sparse count matrices and Seurat analysis. Adapt the lists for a narrower task. Run the block in R. It installs missing packages into the active R library and leaves existing installations available for verification. Select a reachable CRAN mirror. For mainland China, the official mirror list includes `https://mirrors.tuna.tsinghua.edu.cn/CRAN/`. [CRAN mirrors](https://cran.r-project.org/mirrors.html) · [Seurat](https://satijalab.org/seurat/) · [GEOquery](https://bioconductor.org/packages/GEOquery)

```r
options(repos = c(CRAN = "https://cloud.r-project.org"))
cran_pkgs <- c("BiocManager", "Seurat", "Matrix", "ggplot2", "writexl")
bioc_pkgs <- c("GEOquery", "SingleCellExperiment")

missing_cran <- setdiff(cran_pkgs, rownames(installed.packages()))
if (length(missing_cran)) install.packages(missing_cran)

missing_bioc <- setdiff(bioc_pkgs, rownames(installed.packages()))
if (length(missing_bioc)) {
  BiocManager::install(missing_bioc, ask = FALSE, update = FALSE)
}
```

Use this read-only load check after installation or in an existing environment. Add the packages required for the selected branch. A failed load can indicate an incompatible installed dependency. Inspect the underlying error with `library(package_name, character.only = TRUE)` after assigning the failed name to `package_name`.

```r
packages <- c("BiocManager", "Seurat", "Matrix", "ggplot2", "writexl",
              "GEOquery", "SingleCellExperiment")
package_version <- function(pkg) {
  if (requireNamespace(pkg, quietly = TRUE)) as.character(packageVersion(pkg))
  else "missing or failed to load"
}
print(data.frame(package = packages,
                 version = vapply(packages, package_version, character(1)),
                 row.names = NULL))
```

## Add packages for the chosen input or analysis

Install CRAN packages with `install.packages()` and Bioconductor packages with `BiocManager::install()` using their exact names. Check the release page and the upstream installation guide for other sources. Select the reader for the actual file type and verify the expression layer after import.

| Input or task | Packages, source and additional inputs |
|---|---|
| 10x MTX, 10x H5, RDS, H5AD | Seurat reads 10x MTX with `Read10X()`. Its 10x H5 reader uses `hdf5r` (CRAN), with HDF5 development libraries when compiling from source. For RDS use `readRDS()` and the package defining the stored object. For H5AD use `zellkonverter` (Bioconductor) or Python `anndata` in a compatible environment. [10x H5 reader](https://satijalab.org/seurat/reference/read10x_h5) · [hdf5r](https://cran.r-project.org/web/packages/hdf5r/index.html) · [zellkonverter](https://bioconductor.org/packages/zellkonverter) |
| Droplet calling, doublets, ambient RNA | Use `DropletUtils` for raw droplet counts, `scDblFinder` for doublet assessment by capture (both Bioconductor), and `SoupX` (CRAN) when the required droplet and cell inputs are available. [DropletUtils](https://bioconductor.org/packages/DropletUtils) · [scDblFinder](https://bioconductor.org/packages/scDblFinder) · [SoupX](https://cran.r-project.org/web/packages/SoupX/index.html) |
| Integration and reference labels | Use the installed Seurat API for CCA, RPCA or label transfer. `harmony` (CRAN) supports the Harmony branch. `SingleR` (Bioconductor) needs a labeled reference such as a suitable dataset from `celldex` (Bioconductor). Check species, tissue and label resolution. [Integration](https://satijalab.org/seurat/articles/seurat5_integration) · [SingleR](https://bioconductor.org/packages/SingleR) · [celldex](https://bioconductor.org/packages/celldex) |
| Composition and expression | Sample-level proportions can be summarized in R. Choose a design-compatible composition model such as `speckle` where applicable. Use `miloR` for neighborhood abundance and `edgeR` or `DESeq2` for raw-count pseudobulk. These packages come from Bioconductor. [speckle](https://bioconductor.org/packages/speckle) · [miloR](https://bioconductor.org/packages/miloR) · [edgeR](https://bioconductor.org/packages/edgeR) · [DESeq2](https://bioconductor.org/packages/DESeq2) |
| Enrichment and signature scores | Bioconductor supplies `clusterProfiler`, `fgsea`, `UCell` and organism annotation packages. Supply tested gene IDs, a compatible identifier map and versioned gene sets. `msigdbr` (CRAN) is one source of gene sets. [clusterProfiler](https://bioconductor.org/packages/clusterProfiler) · [fgsea](https://bioconductor.org/packages/fgsea) · [UCell](https://bioconductor.org/packages/UCell) |
| Trajectories, velocity and lineage tracing | `slingshot` (Bioconductor) uses a biologically justified trajectory and root. Python `scvelo` needs spliced and unspliced counts. Lineage reconstruction needs matched heritable marks and a tool for that assay, such as Cassiopeia for suitable lineage-tracing data. [slingshot](https://bioconductor.org/packages/slingshot) · [scVelo](https://scvelo.readthedocs.io/en/stable/installation.html) · [Cassiopeia](https://cassiopeia-lineage.readthedocs.io/en/latest/installation.html) |
| Regulation, communication and bulk deconvolution | Python pySCENIC needs matched TF lists, motif annotations and ranking databases. LIANA+ uses a species-appropriate ligand-receptor resource. For a separate bulk cohort, MuSiC is an R option distributed through the authors' GitHub repository and requires a matched multi-subject single-cell reference. [pySCENIC](https://pyscenic.readthedocs.io/en/latest/installation.html) · [LIANA+](https://liana.readthedocs.io/en/stable/) · [MuSiC](https://github.com/xuranw/MuSiC) |
| Expression programs, reference searches and virtual perturbations | Choose cNMF, scGPT, SCimilarity, Geneformer or scTenifoldKnk according to the question, species and available inputs. Install each Python model in its own compatible environment and obtain its stated assets. Record the package and checkpoint revision. [Model prerequisites and workflows](models.md) |

## Prepare an optional Python branch

Choose a Python version supported by the selected tool and checkpoint. For example, create a dedicated cNMF environment from the project directory and use that environment's interpreter directly. Use the upstream environment recipe when a tool specifies particular PyTorch, CUDA or compiled-library builds. [Model-specific setup](models.md) · [Python virtual environments](https://docs.python.org/3/library/venv.html)

**Windows PowerShell**

```powershell
python -m venv .venv-cnmf
.\.venv-cnmf\Scripts\python.exe -m pip install cnmf
.\.venv-cnmf\Scripts\python.exe -m pip check
```

**macOS or Linux**

```sh
python3 -m venv .venv-cnmf
.venv-cnmf/bin/python -m pip install cnmf
.venv-cnmf/bin/python -m pip check
```

For reproducibility, save the R session information with the results. For each Python branch record the interpreter, dependency versions, resource releases, seeds and hardware used. Preserve the mapping between exported cell IDs, input layers and the primary analysis object.
