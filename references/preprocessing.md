# 下载、质控、聚类与细胞注释

每个入选队列使用独立的 `<GSE>_GEO_single-cell_analysis_project/`。下文路径均相对于该目录。续接已有项目时先定位输入、版本和已确认的决定，从适用阶段继续。

## 下载与识别表达层

建立 `raw_data/`、`clean_data/`、`scripts/`、`results/`、`report/` 并在项目中文 README 中注明用途。优先用 GEOquery 获取样本信息。核对 GSE、各 GSM 补充文件和作者关联仓库，下载矩阵、feature 表、barcode、样本分组、细胞元数据、作者注释及说明。原件按文库存入 `raw_data/<GSE>/`，在同目录 `download_log.txt` 中记录来源、时间、大小、路径、状态和可用校验值。

核实物种、scRNA 或 snRNA、技术、矩阵轴向与 RNA 表达层。检查 10x MTX 三件套或 H5/H5AD/RDS/文本矩阵的实际内容，多模态数据取 Gene Expression。结合作者处理记录和数值核验每个表达层。10x filtered 表示细胞筛选，可能仍保留 UMI counts。H5AD 的 `.raw`、`X` 和 `layers["counts"]` 均需核实。记录矩阵维度、条形码数、已识别细胞数、样本数和可确认供体数。

| 可核实的输入 | 可继续的工作 |
|---|---|
| 未归一化基因 counts | 保留完整基因的稀疏 counts，用于计算 QC、适用的归一化及后续供体级分析。 |
| 仅有已归一化 RNA | 记录变换方式和作者 QC。直接使用兼容表达层做聚类、marker 或打分。需要原始计数的步骤标记输入缺失。 |
| 仅有缩放值、整合层、坐标或作者标签 | 复用可核实的坐标、cluster、标签及作者证据。有可靠细胞到样本映射可汇总组成。区分在本地重算与引用作者结果的项目。 |
| 仅 FASTQ | 查作者关联仓库是否有矩阵。仍缺矩阵则登记“待定量”，批量任务继续其他队列。 |

保存下载脚本 `scripts/01_download_check_scRNA.R` 和 `report/下载核验.md`。

## 建立质控前对象

- 保留 feature ID、原始版本后缀、Symbol、物种和参考版本。用稳定唯一键建对象，用匹配版本的注释补充映射并标记重复、一对多与未映射项。
- `clean_data/sample_manifest.csv` 每行一个生物样本，含 `sample`、`donor`、`condition`、`batch`、`tissue`、`technology`。`clean_data/library_map.csv` 记录 `library_id`、`capture_id` 和样本的实际对应。一份混样文库可以包含多个供体，必须有可靠拆样结果才能指派供体。
- 以文库或原始矩阵的唯一命名空间加原 barcode 生成 `cell_id`，核查跨文库重名、同一细胞的重复测序及未匹配记录。将可追溯的样本信息、作者原始 cluster、标签和 QC 字段写入 `clean_data/cell_metadata.csv`。供体未知的细胞单列。
- 含空液滴时，保存细胞识别的方法、条形码判定及数量衔接。以已识别细胞为 QC 分母。记录作者已有过滤的范围，保存 `clean_data/<GSE>_preQC.rds`、`scripts/02_prepare_scRNA.R` 与 `report/输入与映射.md`。本步保留所有候选细胞。

## 第一次确认：逐样本质控方案

1. 有 RNA counts 时计算 `nCount_RNA`、`nFeature_RNA`、`percent.mt`。核实物种和线粒体基因映射，无法识别时将线粒体比例记为缺失。按样本输出分布图及计数与检测基因数散点图。结合组织、细胞或细胞核、各样本分布解释阈值。无 counts 时评估可核实的作者 QC。
2. 按独立捕获批次评估 doublet，在有适配液滴数据时评估环境 RNA，逐细胞保存风险标记。列出每样本各规则命中数、合并去重后预计剔除与保留数、比例，以及预计损失集中的供体或谱系。沿用作者 QC 也应写明依据。
3. 将图、细胞标记及逐样本汇总放 `results/QC/`，脚本放 `scripts/03_QC_review.R`，将 GSE、输入对象版本、方案版本、建议阈值和预计影响写入 `report/QC_review.md`。向用户展示方案，等待对该版本的实际确认。已有相符确认可复用。阈值发生变化时重新展示预计影响。
4. 确认后从对应 preQC 对象执行一次过滤或沿用作者 QC，保留原始 counts（如有）、ID 和元数据。保存每细胞决定与原因，将实际数同预计数逐样本核对，差异追溯到规则。对象按样本放 `clean_data/QC_filtered/`，实绩放 `results/QC/`。同版重跑可复用结果，改版从 preQC 重建依赖的结果。

## 整合、聚类与 marker

根据计数技术选 LogNormalize 或适用于 UMI 的 SCTransform；已归一化表达按其尺度直接使用。保留未整合 PCA、邻居图、UMAP 及聚类，按 sample、donor、condition、cluster 着色。仅在技术批次有依据且存在共享群体时考虑 RPCA、CCA 或 Harmony。对照技术混合、已知 marker、生物状态和单一供体主导情况，允许选用未整合结果。组别与批次完全重合的对比限于描述。

在选定空间构图和聚类，比较至少三个适宜的 resolution，记录各群大小、拆并和样本、供体、条件构成。声称稳定性时用随机种子或重采样复核。按最终 cluster 在可解释的归一化 RNA 层计算 marker。Seurat v5 的 RNA 层仍按样本拆分时先 `JoinLayers()`。采用 SCT 后需标准 RNA 归一化层时，从保留的 RNA counts 生成。导出每群 marker 表（含 log2FC、群内外表达比例和适用调整 P 值）、DotPlot、FeaturePlot 和 Top marker 热图。

保存 `clean_data/<GSE>_clustered.rds`、`results/clustering/`、`results/markers/`、`scripts/04_integrate_cluster_markers.R` 及 `report/聚类与marker分析报告.md`。已核实的作者结果也可作为后续注释入口，注明其来源与限制。

## 第二次确认：细胞类型映射

针对每个 cluster 汇总组织适配的阳性及矛盾 marker、作者标签、异质性、供体构成、候选类型、备选及置信度。作者只提供可信逐细胞标签时，可按其原标签核验。混合谱系信号要核查同一细胞共表达、环境 RNA、混合群和捕获批次 doublet 评分。分别保存 `doublet_flag` 与 `celltype`。有匹配参考时可用 SingleR 或 Seurat 标签转移对照，需用 scGPT 映射或 SCimilarity 检索时查阅[模型与表达程序](models.md)。

输出 `results/annotation/annotation_review.csv`，记录 GSE、映射版本、原 cluster 或作者标签、候选、证据及未解决项，附可用的 marker 证据图与候选 UMAP。用户实际确认此版映射后，记录人工修改，保留原 cluster 和作者原标签，新增 `celltype`；未确认的条目标记 `Uncertain`。交付最终映射、`clean_data/<GSE>_annotated.rds`、逐细胞元数据、逐样本各类型数量和比例、可用注释图、执行脚本及中文报告。
