# 论文阅读笔记

## Neural Network Structure Optimization by Simulated Annealing

生成日期：2026-07-06

## 一、关键词卡片

| 维度 | 内容 |
|------|------|
| 研究问题 | 如何在不使用反向传播（back-propagation）的情况下，通过优化网络结构（即剪枝后保留哪些连接配置）来压缩全连接神经网络并尽量保持性能？ |
| 技术手段 | 模拟退火（Simulated Annealing, SA）、网络剪枝（edge-level 边级剪枝）、mask 矩阵、Markov chain、Boltzmann 接受准则、Metropolis loop |
| 实验范式 | 在 MNIST 与 FASHION 数据集上对浅层全连接网络（4 层）进行剪枝 + SA 结构优化，与随机剪枝和 min-K 阈值剪枝基线对比不同剪枝率下的精度 |
| 数据分析方法 | Boltzmann 概率接受/拒绝、几何冷却（T_{n+1}=η·T_n）、Metropolis loop 长度调参、权重幅值直方图分析、精度随剪枝率变化曲线、时间复杂度随网络规模分析 |
| 主要结论 | (1) SA 可在不进行反向传播的情况下找到近最优剪枝配置，在 90% 剪枝率内恢复大部分精度（如 90% 剪枝时损失从 20%+ 降至约 4%）；(2) 小权重不一定不重要，权重幅值与重要性的相关性随剪枝加深而减弱；(3) 仅前向传播即可在低算力设备本地完成剪枝。 |
| 创新点 | 将 SA 用于网络结构优化（选择保留哪些连接配置）而非权重更新；直接以网络损失函数为目标、无需反向传播；通过 mask 矩阵置换实现连接配置搜索；实验证明权重幅值不能单独判定重要性。 |

## 二、Abstract

### 原文（英文）

A critical problem in large neural networks is over parameterization with a large number of weight parameters, which limits their use on edge devices due to prohibitive computational power and memory/storage requirements. To make neural networks more practical on edge devices and real-time industrial applications, they need to be compressed in advance. Since edge devices cannot train or access trained networks when internet resources are scarce, the preloading of smaller networks is essential. Various works in the literature have shown that the redundant branches can be pruned strategically in a fully connected network without sacrificing the performance significantly. However, majority of these methodologies need high computational resources to integrate weight training via the back-propagation algorithm during the process of network compression. In this work, we draw attention to the optimization of the network structure for preserving performance despite compression by pruning aggressively. The structure optimization is performed using the simulated annealing algorithm only, without utilizing back-propagation for branch weight training. Being a heuristic-based, non-convex optimization method, simulated annealing provides a globally near-optimal solution to this NP-hard problem for a given percentage of branch pruning. Our simulation results have shown that simulated annealing can significantly reduce the complexity of a fully connected network while maintaining the performance without the help of back-propagation.

### 中文翻译

大型神经网络的一个关键问题是参数过多，因计算与存储需求过高而限制其在边缘设备上的使用。为使神经网络在边缘设备与实时工业应用中更实用，需预先压缩。由于边缘设备在网络资源稀缺时无法训练或访问已训练网络，预装更小网络至关重要。已有研究表明，全连接网络中的冗余分支可被策略性剪枝而不显著牺牲性能。然而，多数方法在网络压缩过程中仍需通过反向传播进行权重训练，消耗大量计算资源。本文关注通过激进剪枝进行结构优化以在压缩下保持性能。结构优化仅使用模拟退火算法完成，不利用反向传播进行分支权重训练。作为基于启发式的非凸优化方法，模拟退火为给定剪枝比例的 NP 难问题提供全局近最优解。模拟结果表明，模拟退火可在无反向传播辅助下显著降低全连接网络复杂度并保持性能。

## 三、Introduction 各段摘要与行文逻辑

【第1段 · 定位词：The successful development of artificial intelligence】
▸ 主要内容：AI 与深度学习在多行业产生重要影响，但出色表现伴随计算复杂度代价；神经网络需经历初始化、反向传播、梯度更新等训练步骤，结构维度增大则参数与运算量随之增加。
  引用文献：[1,2][3,4][5][6–8]

【第2段 · 定位词：Neural network compression is a relatively】
▸ 主要内容：网络压缩是因深度网络发展与边缘设备有限算力而兴起的新领域；将主流压缩策略归为四类：(i) 量化降低位数、(ii) 层分解/简化激活函数、(iii) 知识蒸馏、(iv) 剪枝增加稀疏性。
  引用文献：[9][10][11][12,13]

【第3段 · 定位词：In this work, we concentrate on】
▸ 主要内容：本文聚焦第四类剪枝，提出微观尺度（edge 级）的网络结构优化新方法，区别于优化宏观架构性能但不一定压缩网络的其他工作。
  引用文献：[14,15]

【第4段 · 定位词：The main idea of pruning is】
▸ 主要内容：批评"小权重即不重要"的常见假设——小权重可能通向大权重分支，网络高度非线性使难以仅凭权重大小判断重要性；指出多数现有剪枝方法仍依赖反向传播与梯度更新，消耗大量计算资源。
  引用文献：[16]

【第5段 · 定位词：The direct pruning methods mentioned】
▸ 主要内容：综述直接剪枝与梯度剪枝方法（近端梯度算法、二值门控近似、梯度阈值剪枝、反向更新权重剪枝），均需强力计算机与梯度下降；指出仅置零不能真正减小存储，需直接剪枝权重参数（element-wise/vector-wise/block-wise）。
  引用文献：[17][18][19][20][21]

【第6段 · 定位词：Since a neural network is composed】
▸ 主要内容：从网络由节点与边构成的视角，将剪枝分为结构化（node-level，删节点连带删所有连接边）与非结构化（edge-level，仅删单条边，用 mask 矩阵控制），分别以节点级与边级为代表。
  引用文献：[22,23][24,25][26,27][28]

【第7段 · 定位词：In choosing pruning strategies】
▸ 主要内容：指出现有剪枝方法两大缺点——不强调节省计算资源、不考量结果网络结构的最优性；提出用 SA 优化分支连接配置（在固定剪枝率下），将剪枝配置置换视为有限 Markov 链，直接以损失函数为目标，保证找到固定参数下的最优置换配置。
  引用文献：无（方法提出段）

▸ 行文逻辑总结：从"深度学习计算复杂度高、边缘设备需压缩"的大背景出发，梳理四类压缩策略并聚焦剪枝，进而批评"小权重不重要"假设与"剪枝仍依赖反向传播"的痛点，再从结构化/非结构化剪枝分类引出"优化连接配置"的需求，最终提出用 SA 在固定剪枝率下搜索最优连接配置——由背景到痛点到方法，逻辑层层聚焦。

## 四、Methods 摘要

- **被试**：本文不涉及人类被试。使用 MNIST 与 FASHION 两个开源数据集（各 >50k 图像、10 类）；实验网络为简单的 4 层全连接浅层网络（Figure 3），仅在隐藏层剪枝以便清晰验证方法有效性。
- **实验范式**：剪枝 + SA 结构优化——先训练全连接网络，按剪枝率 p 随机剪枝，再用 SA 优化 mask 矩阵（搜索保留哪些连接），与随机剪枝和 min-K 阈值剪枝基线对比不同剪枝率下的精度。
- **实验流程**：

1. 用梯度下降训练全连接网络得到权重 w、偏置 b
2. 按剪枝率 p 随机剪枝隐藏层边（生成初始 mask 矩阵 M）
3. 执行 SA（Algorithm 1）：在 Metropolis loop 内随机选一条已连接边与一条已断开边交换连接状态，计算新损失，按 Boltzmann 准则接受/拒绝
4. 几何冷却（T←η·T）重复 Metropolis loop 直至 T<T_min
5. 在 MNIST/FASHION 评估最终配置精度，与基线对比

- **数据分析方法**：

SA 三大机制设计——(1) 状态邻域结构：mask 矩阵中同行移动一个 0/1 置换（保守邻域，可扩展为多置换）；(2) 接受-拒绝准则：Boltzmann 概率 P_b=min(1, exp(−ΔL/(k·T)))，差解以概率接受以跳出局部最优；(3) 冷却方案：几何冷却 T_{n+1}=η·T_n
收敛性——基于 Markov 链 detailed balance 证明收敛到唯一平稳分布（随温度降低分布愈发集中于最优解）
权重直方图分析——对比 min-K 与 SA 在不同保留比例下的权重幅值分布
时间复杂度分析——随 MLL、剪枝率、网络规模（边数 10^0~10^4）的变化

## 五、Results 逐一对应

[1] 分析方法：权重参数选择可视化（4.1，Figures 4、5）
→ 结果：min-K 剪枝的权重分布始终集中在均值附近（小幅值权重）；SA 剪枝初期也按幅值相关性选择，但随着剪枝加深，被保留的权重分散到高幅值区域，相关性减弱。
→ 结论：权重幅值与重要性的相关性随剪枝加深而减弱，证明小权重不一定不重要，SA 能发现幅值之外的重要性信号。

[2] 分析方法：不同剪枝率下的性能趋势（4.2，Figures 6–9）
→ 结果：MNIST 上 SA（MLL>20）在 90% 剪枝率内恢复大部分精度，90% 剪枝时损失从 20%+ 降至约 4%；99% 剪枝时仍显著优于随机与 min-K；FASHION 上类似规律但绝对精度较低；MLL=50 是兼顾性能与时间的稳妥选择；剩余权重<30% 时 SA 优势尤为明显。
→ 结论：SA 在固定权重下能有效找到近最优连接配置，尤其在高剪枝率（剩余<30%）时价值突出，且效果独立于网络原始精度。

[3] 分析方法：SA 剪枝的时间复杂度（4.3，Figures 10、11）
→ 结果：MLL 20–50 足够；T_init=0.2、η=0.95、100–150 次温度更新后收敛；网络规模增大 10 倍时间增 1.2 倍、增大 10^4 倍时间增 9 倍（亚对数增长）；仅前向传播无需梯度，节省大量内存。
→ 结论：SA 剪枝时间复杂度随网络规模亚对数增长，可在低算力设备（如 Intel i3 + 3GB RAM）本地完成，无需云端。

▸ 行文逻辑总结：先以权重直方图揭示 SA 与 min-K 的本质差异（幅值相关性减弱），再以精度-剪枝率曲线量化 SA 的恢复能力与适用范围（高剪枝率优势），最后以时间复杂度评估落地可行性——从机制到效果到工程可行性，层层递进。

## 六、Discussion 各段摘要与行文逻辑

【第1段 · 定位词：Even though there are limits determined】
▸ 主要内容：承认浅层全连接网络性能上限（不如 VGG/ResNet，因卷积提特征更高效），但指出卷积可转为矩阵乘法故全连接网络潜力可由更好的权重更新方法发掘；SA 所得全局最优仅针对固定参数，但置换配置可超越经典幅值阈值剪枝；实验证明小幅值权重不一定不重要，SA 选关键权重可在不牺牲性能下获更轻量配置。
  引用文献：[53]

【第2段 · 定位词：The other advantage of our work】
▸ 主要内容：强调 SA 剪枝仅含前向传播、节省 RAM、可在低算力设备本地完成无需云端的实用价值（如医疗行业数据量大但算力不足的场景）；指出方法可扩展性——重定义状态空间与邻域结构即可用于 node-level 或卷积 filter 剪枝（问 SA 该删哪个 filter），借助 GPU 可将复杂网络剪枝时间降至可接受水平。

▸ 行文逻辑总结：先承认局限（浅层网络性能上限）并解释原因，再阐明 SA 优化的本质价值（固定参数下的最优配置超越幅值剪枝），最后展望实用价值（本地剪枝、医疗场景）与可扩展性（node/filter 级、GPU 加速），遵循"局限→价值→应用前景"的讨论逻辑。

## 七、我的阅读笔记（待填写）

【核心贡献与意义】



【与我研究的关联】



【方法借鉴点】



【疑问与待深入之处】



【其他备注】

