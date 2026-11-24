# 生信 单细胞分析技能

面向 GEO 多样本单细胞和单核 RNA-seq 的中文 Codex 技能。可以从公开队列检索开始，也可以把已有的表达矩阵、Seurat 或 AnnData 对象交给它，从质控、注释或组间比较接着做。

## 安装到研究项目

在项目根目录运行以下命令，再在该项目的 Codex 对话中使用 `$geo-single-cell-analysis`。

```shell
git clone https://github.com/rushou21/geo-single-cell-analysis.git .agents/skills/geo-single-cell-analysis
```

技能提供工作流说明。实际分析依照任务使用 R、Seurat 和相应的统计包，扩展方法按需使用匹配版本的 Python 环境、参考图谱或模型权重。

## 使用示例

> 用 $geo-single-cell-analysis 检索人类肾组织的病例与对照 scRNA-seq 队列，核实每组的独立供体数、细胞级表达矩阵和作者注释，按适合供体级比较的程度评分，交付候选表。

> 用 $geo-single-cell-analysis 从已定稿细胞类型的 Seurat 对象继续。先核对 RNA 表达层、供体配对和细胞覆盖，再比较各类型比例，并对有原始 counts 的类型做 pseudobulk 差异表达。

## 分析范围

| 阶段 | 交付与说明 |
|---|---|
| [GEO 检索与评分](references/selection.md) | 逐条核实官方记录，按图谱或病例对照用途评分，并对重复发布的队列去重。 |
| [输入、质控与注释](references/preprocessing.md) | 区分原始 counts、归一化数据和作者已有结果。全流程先展示各样本的预计 QC 影响，再按确认的方案过滤。候选细胞标签经确认后定稿。 |
| [供体级比较](references/downstream.md) | 按独立生物学重复评估细胞组成、类型内差异表达与通路变化，按数据条件开展拟时序、调控网络和细胞通讯等分析。 |
| [表达程序与模型](references/models.md) | 用 cNMF 发现表达程序，用 scGPT 或 SCimilarity 辅助核查身份与状态，用 Geneformer 或 scTenifoldKnk 探索虚拟扰动，并标明预测的解释范围。 |

完整入口见 [SKILL.md](SKILL.md)。本仓库的技能文本使用 [MIT 许可证](LICENSE)。外部数据、图谱和模型权重分别适用各发布方的条款。
