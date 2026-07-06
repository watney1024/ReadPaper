# 论文阅读笔记

## Sparse neural network optimization by Simulated Annealing

生成日期：2026-07-06

## 一、关键词卡片

| 维度 | 内容 |
|------|------|
| 研究问题 | 如何在不依赖反向传播的情况下，同时优化稀疏神经网络的结构（拓扑）和权重参数，以获得全局最优的稀疏网络？ |
| 技术手段 | 计算建模（Simulated Annealing 优化）、全连接网络(FCN)与卷积神经网络(CNN)实验、图像分类数据集实验 |
| 实验范式 | 在 FASHION 和 CIFAR10 数据集上，用 SA 逐层优化网络权重和结构，与反向传播(BP)基线对比准确率与时间消耗 |
| 数据分析方法 | SA 随机游走优化, Boltzmann 接受/拒绝机制, 几何冷却方案, 逐层优化策略, 不同稀疏度对比实验, Bootstrapping vs Random Walk 对比 |
| 主要结论 | 1) SA 联合优化稀疏网络结构和权重可超越 BP 训练的网络性能（尤其在高稀疏度 >85% 时），挑战了 BP 的全局最优性；2) 仅用单卷积层即可达 88% 训练精度，稀疏网络测试集提升约 3% |
| 创新点 | 首次将稀疏网络结构优化与权重参数优化合并为统一的 SA 框架（离散+连续空间统一），无需反向传播即可训练，并提供全局最优性保证 |

## 二、Abstract

### 原文（英文）

The over-parameterization of neural networks and the local optimality of backpropagation algorithm have been two major problems associated with deep-learning. In order to reduce the redundancy of neural network parameters, the conventional approach has been to prune branches with small weights. However, this only solves the problem of parameter redundancy, not providing any global optimality guarantees. In this paper, we overturn back-propagation and combine the sparse network optimization problem and the network weight optimization problem using a non-convex optimization method, namely Simulated Annealing. This method can complete network training under the premise of controlling the amount of parameters. Different from simply updating network parameters using gradient descent, our method simultaneously optimizes the topology of the sparse network. With the guarantee of global optimality of Simulated Annealing solution, the performance of the sparse network optimized by our method has exceeded the one trained by backpropagation only.

### 中文翻译

神经网络的过参数化和反向传播算法的局部最优性是深度学习相关的两大主要问题。为了减少神经网络参数的冗余，常规方法是剪枝权重较小的分支。然而，这仅解决了参数冗余问题，并未提供任何全局最优性保证。在本文中，我们颠覆反向传播，采用一种非凸优化方法——模拟退火（Simulated Annealing），将稀疏网络优化问题与网络权重优化问题相结合。该方法可在控制参数数量的前提下完成网络训练。与仅用梯度下降更新网络参数不同，我们的方法同时优化稀疏网络的拓扑结构。在模拟退火解的全局最优性保证下，由我们方法优化的稀疏网络性能已超越仅由反向传播训练的网络。

## 三、Introduction 各段摘要与行文逻辑

【第1段 · 定位词：The game changing observation that】
▸ 主要内容：深度学习自 2012 年（AlexNet、VGG、ResNet）快速发展，但这些网络参数量巨大（ResNet18 超 11M、VGG16 超 138M），为后续问题铺垫背景。
  引用文献：Krizhevsky, 2012; Simonyan, 2015; He, 2016

【第2段 · 定位词：A neural network is effectively a】
▸ 主要内容：神经网络是高维非凸函数，参数量大导致易陷入局部最优、内存与计算资源需求高，难以在便携设备上部署。
  引用文献：

【第3段 · 定位词：The overwhelmingly common approach for】
▸ 主要内容：反向传播（梯度下降）是最常用参数优化方法，minibatch、momentum 等改进降低了陷入局部最小的概率，但仍无法保证收敛到全局最优。
  引用文献：Li, 2014; Kingma, 2015; Dauphin, 2015

【第4段 · 定位词：A far less researched approach is】
▸ 主要内容：介绍启发式算法替代方案（GA、PSO、SA），分为顺序型和并行型。SA 为顺序搜索，虽慢但内存占用低，更适合资源受限场景。
  引用文献：Sastry, 2005; Das, 2008; Han, 2010; Wang, 2020; Laarhoven, 1987; Rere, 2015

【第5段 · 定位词：In addition to the problem of】
▸ 主要内容：参数冗余是另一关键问题，已知剪枝 90% 分支不会显著降低性能，引出剪枝方法综述。
  引用文献：Frankle, 2019

【第6段 · 定位词：Based on the hierarchical characteristic of】
▸ 主要内容：剪枝方法分类——非结构化（边级/节点级，多用于 FCN）与结构化（通道级/滤波器级，多用于 CNN）。
  引用文献：Cho, 2021; Hoefler, 2021; He, 2014; LeCun, 1989; Hassibi, 1992

【第7段 · 定位词：The existing pruning methods follow】
▸ 主要内容：三种剪枝流程：one-shot pruning、GPAT（训练后渐进剪枝）、GPWT（训练中渐进剪枝），各有时间效率与性能权衡。
  引用文献：

【第8段 · 定位词：As exemplified in deep compression】
▸ 主要内容：深度压缩方法以权重幅值为阈值剪枝，剪枝后微调；但稀疏矩阵仍占空间，需紧致压缩将稀疏矩阵转为小密集矩阵。
  引用文献：Han, 2015; Chen, 2020

【第9段 · 定位词：[21] states that the small】
▸ 主要内容：权重幅值小不等于不重要，梯度大小也是重要性指标；现有剪枝方法多依赖反向传播和梯度更新。
  引用文献：Victor, 2020; Shih-Kang, 2020; Shulman, 2020

【第10段 · 定位词：In choosing pruning strategies, the】
▸ 主要内容：指出现有剪枝方法两大缺陷：不注重计算资源节省、不考虑网络结构最优性。本文目标是优化分支连接。
  引用文献：

【第11段 · 定位词：Some recent work propose to】
▸ 主要内容：近期基于梯度的剪枝方法：sparse momentum、自动稀疏连接学习、AutoSparse、Class-Aware Trace Ratio Optimization；综述表明现代方法未必超越早期方法。
  引用文献：Dettmers, 2019; Tang, 2022; Kundu, 2023; Hu, 2021; Blalock, 2020

【第12段 · 定位词：All of these work have in】
▸ 主要内容：总结上述方法共性——基于局部变量阈值、未声明全局最优、均依赖反向传播，聚焦于剪枝。
  引用文献：

【第13段 · 定位词：Other than the mechanisms that highly】
▸ 主要内容：少数基于启发式的网络优化工作：GA 优化网络架构、ABC 算法擦除通道参数、作者前期工作[31]用 SA 优化结构、[20]用 SA 减少硬件内存需求。
  引用文献：Wang, 2020; Lin, 2020; Kuo, 2022; Chen, 2020

【第14段 · 定位词：Although these methods can reduce】
▸ 主要内容：现有方法依赖梯度下降训练权重，存在局部最优风险；权重更新后需重新优化结构，迭代代价高。本文扩展前期工作[31]，提出联合优化权重与结构。
  引用文献：Kuo, 2022

【第15段 · 定位词：As for the papers which avoid】
▸ 主要内容：对比避免 BP 的工作：[12] 忽略结构优化，[31] 不更新权重。本文用 SA 统一拓扑优化、权重更新和冗余分支消除，SA 提供全局最优保证（GA、PSO 无此保证）。
  引用文献：Rere, 2015; Kuo, 2022

【第16段 · 定位词：We would like to mention here】
▸ 主要内容：区分本文与 NAS 研究：NAS 关注宏观结构设计，本文关注微观分支层面；本文求解给定剪枝率下的优化问题，而非自动寻找理想剪枝率。
  引用文献：

▸ 行文逻辑总结：从深度学习参数冗余的大背景出发 → 指出反向传播的局部最优缺陷 → 介绍启发式算法替代方案 → 综述参数剪枝方法及其两大缺陷 → 指出现有方法均依赖 BP 且无全局最优保证 → 引出本文基于 SA 的联合优化方案，逐步聚焦到"用 SA 同时优化稀疏网络结构和权重"这一具体研究问题，最后与 NAS 区分界定研究范围。

## 四、Methods 摘要

- **被试**：无被试（计算实验）
- **实验范式**：在 FASHION（60000 张 28×28 灰度图）和 CIFAR10（60000 张 32×32 彩色图）数据集上，用 SA 算法逐层优化 FCN 和 CNN 的权重参数与网络结构，与反向传播基线对比准确率与时间消耗。两网络除第一层外参数完全相同。
- **实验流程**：

1. 预训练网络（用反向传播初始化除第一层外的权重）
2. 选取单层用 SA 优化：在 Markov chain 随机游走中同时更新权重值和非零权重位置
3. 每步计算损失，按 Boltzmann 概率接受/拒绝新状态（接受更优解，以一定概率接受较差解以逃离局部最优）
4. 几何冷却方案逐步降温至 Tmin 停止
5. 扩展到三层联合优化

- **数据分析方法**：

1. SA 随机游走优化（结构空间 + 权重空间同时步进）
2. Boltzmann 接受/拒绝机制
3. 几何冷却方案
4. 逐层优化策略
5. 不同稀疏度（0% / 50% / 70% / 95%）对比实验
6. Bootstrapping（无记忆随机源）vs Random Walk（有记忆随机源）对比
7. 时间消耗分析（FCN/CNN × FASHION/CIFAR10）

## 五、Results 逐一对应

[1] 分析方法：Bootstrapping（无记忆随机游走）vs BP
→ 结果：CNN 用 bootstrapping 更新权重，准确率可达 BP 水平；Nch（每次改变权重数）取 8、3、1 中，Nch=1 效果最好
→ 结论：权重更新步长越小越好；纯随机源缺乏记忆结构，学习能力有限

[2] 分析方法：Random Walk（有记忆随机游走）vs BP
→ 结果：RW 显著提升性能；稀疏网络比密集网络收敛更快；密集 CNN 准确率超 BP 5%；但训练集超越 BP 而测试集落后，存在过拟合
→ 结论：有记忆的随机游走使 SA 能有效从数据学习；稀疏网络因结构可调获得更快收敛速度

[3] 分析方法：不同稀疏度下 SA vs BP（单层/多层）
→ 结果：稀疏度 >85% 时 SA 在训练集和测试集均超越 BP；优化三层后，50% 稀疏度即可在训练集超越 BP（如 50% 稀疏度 SA 三层 84.4%/62.4% vs BP 73.2%/62.2%）
→ 结论：高稀疏度下结构和权重联合优化优势明显，验证了反向传播的次优性

[4] 分析方法：时间消耗分析
→ 结果：FCN(FASHION) 96min，CNN(FASHION) 105min，CNN(CIFAR10) 310min（10000 次温度更新）；CNN 比 FCN 慢（需额外变换函数），CIFAR10 比 FASHION 慢约 3 倍（输入节点多）
→ 结论：SA 计算成本较高但可接受；时间主要受网络类型、数据集规模、随机源类型影响

▸ 行文逻辑总结：先验证算法基本可行性（bootstrapping 能达 BP 水平）→ 改进随机源（RW）显著提升性能 → 在不同稀疏度下与 BP 系统对比证明 SA 优越性 → 分析时间成本评估实用性，从可行性到优越性到实用性逐步推进。

## 六、Discussion 各段摘要与行文逻辑

【第1段 · 定位词：In this work, we have studied】
▸ 主要内容：总结研究：将稀疏神经网络的结构优化和权重优化统一为一个问题，证明了基于 Markov chain 学习的 SA 方法的成功。

【第2段 · 定位词：An important observation is that】
▸ 主要内容：SA 超越 BP，质疑 BP 的全局最优性；相比 BP 有 50% 内存优势，相比 GA 等启发式方法内存优势更大。

【第3段 · 定位词：We underline that using only】
▸ 主要内容：仅用单卷积层即达 88% 训练精度，与多层 ResNet/VGG 差距在 10% 以内；稀疏网络因同时优化权重和拓扑，测试集提升约 3%。

【第4段 · 定位词：We demonstrated that pruning alone】
▸ 主要内容：剪枝 alone 不能获得最优网络，需结构优化；联合稀疏结构优化与权重参数优化可逼近给定数据下的全局最优神经网络模型。

▸ 行文逻辑总结：概述核心发现（统一优化框架成功）→ SA 超越 BP 的意义（质疑 BP 全局最优性 + 内存优势）→ 单层高效性（接近深层网络性能）→ 剪枝 + 结构优化的必要性（联合优化逼近全局最优）。本文无独立 Discussion 章节，Conclusions 兼作讨论。

## 七、我的阅读笔记（待填写）

【核心贡献与意义】



【与我研究的关联】



【方法借鉴点】



【疑问与待深入之处】



【其他备注】

