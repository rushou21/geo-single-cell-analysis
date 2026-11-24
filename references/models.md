# 表达程序、参考映射与虚拟扰动

注释候选阶段按需要读取 scGPT 和 SCimilarity。确认标签后，优先在有足够细胞的谱系评估 cNMF，再根据待验证的具体状态或候选基因选择检索、扰动分支。已有同一版本输入和参数的结果可以复用。

保留主分析对象。为每个分支记录表达层、矩阵方向、物种、基因 ID、映射覆盖及细胞 ID。Seurat 转 AnnData 时核对转置后的行列名、维度和每个细胞的 counts 总量（若有）。记录软件、权重、参考索引、种子、资源及脚本。将运行状态、产物路径或受限原因写入 `results/analysis_index.csv`。

在调参、选基因及定义目标状态前划分发现与验证供体，同一供体的全部细胞及文库归入同一侧。分别记录参考库和预训练资料与查询队列的重叠情况，无法查证时标为未知。报告中标明证据来自队列内稳定性、独立队列复现、模型预测还是实测干预。

## scGPT 辅助注释

选择与检查点物种、组织和标签粒度相适配且有可信注释的参考。按该检查点的词表和预处理生成参考与查询细胞的嵌入，再依据参考邻居给出候选标签。在相同参考、相同留出供体上与 Seurat 标签转移或 SingleR 比较。具备独立真值时报告宏平均 F1、分类型召回率及拒判率。无真值时报告方法一致性、冲突及 marker 证据，低置信度保留未知。将逐细胞候选、词表覆盖和评估表存入 `results/scGPT/`，随注释审核表提交。[官方参考映射示例](https://scgpt.readthedocs.io/en/stable/tutorial_reference_mapping.html)

## SCimilarity 相似细胞检索

用人类细胞群或状态的可信 RNA counts，按模型要求映射基因名、对齐基因顺序，再执行每细胞一万归一化和 log1p。将近邻距离、候选类型、组织、来源研究、可得供体和支持或矛盾的 marker 保存至 `results/SCimilarity/`。单列来自同一 GSE、重复提交及共享供体的命中。其余跨研究命中作为检索线索，取得独立供体数据后再复核状态及标记。[官方细胞检索示例](https://genentech.github.io/scimilarity/notebooks/cell_search_tutorial_1.html)

## cNMF 表达程序发现

输入 QC 后细胞 × 基因的非负 counts，从完整基因集按方法选择特征。优先在同一谱系内分析状态，有跨谱系问题时扩展到全队列。比较多个程序数 K 和随机初值，结合共识稳定性、重构误差和程序解释选择 K。将程序基因权重、代表基因、每细胞使用量和供体级摘要存入 `results/cNMF/`。检查与测序深度、应激、细胞周期或单一供体的关联。评估外部复现时固定发现集程序，投影留出供体并比较使用量。[官方 cNMF 工作流](https://github.com/dylkot/cNMF)

## Geneformer 虚拟扰动

为同一细胞类型预设候选基因、来源状态以及有依据时的目标状态。核对人类检查点适用范围，以 QC 后全基因 raw counts、相匹配的 Ensembl ID 和每细胞 `n_counts` 供对应版本的 tokenizer 使用。核查序列截断、候选进入序列的细胞数和供体数。按版本确认扰动参数语义，逐个测试候选时每次只提交一个基因。

模拟删除采用移除基因 token，模拟过表达采用提升 token 排名。对照基因按表达量、检出率或排名匹配。将表征位移、方向、有效覆盖及供体间一致性存入 `results/Geneformer/`。有固定目标参考时可解释向该状态的位移，缺少目标状态时只解释一般表征变化。生物学效应需独立干预验证。[官方分词器说明](https://geneformer.readthedocs.io/en/latest/geneformer.tokenizer.html) · [官方虚拟扰动说明](https://geneformer.readthedocs.io/en/latest/geneformer.in_silico_perturber.html)

## scTenifoldKnk 网络虚拟敲除

从目标类型足量、未扰动的基线细胞和基因 × 细胞 counts 建网，核实候选基因有表达且进入网络。逐个运行虚拟敲除，将预测差异调控基因排名、通路及受检背景存入 `results/scTenifoldKnk/`。按供体重采样或分供体重建，评估排名稳定性，加入覆盖相当的对照基因。只有调控差异幅度时按幅度解释。可与 Geneformer 结果对照，同队列两种模型的一致性记为探索性证据。[官方 scTenifoldKnk 说明](https://github.com/cailab-tamu/scTenifoldKnk)
