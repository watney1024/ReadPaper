# 论文阅读笔记

## Retraining-Free Mixed-Precision Quantization for Power Equipment Defect Detection via Layer-Aware Particle Swarm Optimization

生成日期：2026-07-06

## 一、关键词卡片

| 维度 | 内容 |
|------|------|
| 研究问题 | 如何在无需重训练、仅用少量无标签校准数据的前提下，为电力设备缺陷检测的边缘部署模型自动搜索最优混合精度量化（MPQ）配置，以兼顾压缩率与精度？ |
| 技术手段 | 混合精度量化 MPQ、后训练量化 PTQ、粒子群优化 PSO、权重共享 Supernet、Monte Carlo 采样、动态位宽冻结（dynamic bit-width freezing）、轻量特征校准（teacher-student + STE）、非对称均匀量化（权重 per-channel、激活 per-layer） |
| 实验范式 | 在 ImageNet2012 分类与电力设备绝缘子缺陷检测数据集上评估，对比 UniQ/OSME/ACIQ 等基线；消融层重要性引导与 MPQ 贡献 |
| 数据分析方法 | 量化策略评估（量化模型与全精度模型输出的 MSE）、层重要性度量（位宽增益 G_j）、PSO 速度更新（含重要性方向项）、Monte Carlo 采样训练 Supernet、位宽不稳定性评分与 Top-K 余弦退火冻结、特征校准 loss（输出+中间特征） |
| 主要结论 | (1) PSOQ 实现 7.3–7.8x 计算与尺寸压缩、精度偏差<4%，优于现有 PTQ；(2) 仅用 50 个无标签样本评估（比完整测试集省约 2000x 计算）；(3) 在 sub-8-bit 场景显著优于均匀量化（MobileNet-V2：10.12%→68.88%）；(4) 层重要性引导加速 PSO 收敛并提精度。 |
| 创新点 | Supernet + 层重要性引导 PSO 的 retraining-free MPQ 框架；将层重要性作为方向项融入 PSO 速度更新；动态位宽冻结机制（按量化边界不稳定性评分 + Top-K 余弦退火）抑制低比特子网络对共享权重的干扰；轻量特征校准（输出 logits + 中间特征对齐）以无标签数据恢复精度；50 样本无标签评估策略。 |

## 二、Abstract

### 原文（英文）

Traditional deep learning methods have excelled in power equipment defect detection, but their high computational requirements hinder real deployment on edge devices. To address this challenge, this article introduced particle swarm optimization for retraining-free mixed-precision quantization (PSOQ), a novel post-training quantization framework enabling retraining-free mixed-precision quantization, through layer importance-guided particle swarm optimization (PSO) over a one-shot trained Supernet. Specifically, this framework constructed a Supernet using Monte Carlo sampling and interference-aware bit-width scheduling for fast, accurate evaluation of mixed-precision quantization configurations—without fine-tuning. Experiments on benchmark and insulator defect datasets demonstrated that PSOQ, when applied to various network architectures, significantly reduced computational and storage overhead, while maintaining detection accuracy.

### 中文翻译

传统深度学习方法在电力设备缺陷检测中表现出色，但其高计算需求阻碍了在边缘设备上的实际部署。为应对这一挑战，本文提出了基于粒子群优化的免重训练混合精度量化（PSOQ）——一种新颖的后训练量化框架，通过在一次训练的 Supernet 上进行层重要性引导的粒子群优化实现免重训练的混合精度量化。具体而言，该框架利用 Monte Carlo 采样与干扰感知的位宽调度构建 Supernet，以快速、准确地评估混合精度量化配置——无需微调。在基准数据集与绝缘子缺陷数据集上的实验表明，PSOQ 应用于多种网络架构时，在保持检测精度的同时显著降低了计算与存储开销。

## 三、Introduction 各段摘要与行文逻辑

【第1段 · 定位词：As smart grid infrastructure has】
▸ 主要内容：阐述背景——智能电网推进使电力设备（变压器、断路器、绝缘子、避雷器）稳定高效运行愈发关键，设备易出腐蚀/裂纹/放电/过热等缺陷，不及时识别将致大面积停电与安全隐患，故高精度实时缺陷检测系统对现代电网智能化与可靠性至关重要。
  引用文献：Zhao et al., 2025

【第2段 · 定位词：Traditional approaches to detecting】
▸ 主要内容：传统人工巡检效率低、主观偏差大、时空覆盖有限；近年深度学习在图像识别与目标检测驱动下，基于多模态感知（红外热像、高分辨成像、振动、声学）的智能缺陷检测兴起，YOLO/Faster R-CNN/Swin Transformer 在实验与半实景场景表现优异。
  引用文献：Ma et al., 2021

【第3段 · 定位词：Deploying these deep learning models】
▸ 主要内容：指出部署痛点——大规模参数与高计算需求使实时现场推理困难；边缘场景（远距输电线、山区、无人变电站）云推理受连通性差、传输延迟高、数据隐私问题制约。
  引用文献：Ma et al., 2025; Zhao et al., 2025

【第4段 · 定位词：Edge computing has offered a】
▸ 主要内容：边缘计算在数据源附近推理可降通信开销与提升响应，但边缘设备算力/内存/能耗受限，难以部署大规模网络；为此提出剪枝、知识蒸馏、量化等压缩加速技术，其中量化因不改架构、显著降低内存与计算且兼容边缘硬件而突出。
  引用文献：Cao et al., 2019; Khan et al., 2020; Sharif et al., 2023; Cheng et al., 2024; Tang et al., 2024; Li et al., 2023; Zhang et al., 2022; Bashar et al., 2021; Elkordy & Avestimehr, 2022

【第5段 · 定位词：The majority of current quantization】
▸ 主要内容：多数量化技术依赖原始训练数据重训练/微调，实用性受限；电力系统原始图像含敏感/专有信息且受隐私法规限制不可重训练，且重训练大模型成本高不适实时部署；故 PTQ 作为实用低成本替代兴起，仅需少量无标签校准数据直接量化预训练网络，降低部署门槛。
  引用文献：Ma et al., 2022; Chen et al., 2022; Zhang et al., 2025

【第6段 · 定位词：Despite its advantages, however, PTQ】
▸ 主要内容：指出 PTQ 在低于 8 位时性能严重退化——量化噪声随位宽降低剧增，深层/敏感层尤甚；根因是不同层对量化重要性各异，统一位宽无法平衡性能与效率。
  引用文献：Li et al., 2023; Wang et al., 2023

【第7段 · 定位词：Mixed-precision quantization (MPQ) addressed】
▸ 主要内容：MPQ 为不同层分配不同位宽（敏感层高精度、不敏感层低精度）以兼顾效率与精度；但搜索空间指数增长，早期方法假设层间量化误差独立可加而在激进量化下失效；近期 NAS 自动搜索 MPQ 策略精度潜力强但需大规模训练数据与高计算成本，PTQ 场景可行性受限。
  引用文献：Peng et al., 2022; Zhang et al., 2025; Chitty-Venkata et al., 2023; Maman & Schiele, 2025; Peng et al., 2023; Yuan et al., 2020

【第8段 · 定位词：To this end, this study proposed】
▸ 主要内容：提出 PSOQ——结合层重要性引导 PSO 与一次训练 Supernet 的 retraining-free MPQ 框架；Supernet 权重共享使任意 MPQ 配置可快速评估无需重训练；PSO 在层重要性引导下高效探索高维配置空间避免局部最优；仅需约 50 校准样本，可自主依资源约束构建搜索空间，适用数据受限与隐私敏感场景；跨 GPU/NPU/定制加速器可扩展；最后以轻量特征校准进一步精修。
  引用文献：Li et al., 2023

【第9段 · 定位词：The main contributions of this】
▸ 主要内容：列出四项贡献——(1) Supernet+PSO 的 retraining-free MPQ 框架；(2) 层重要性引导的 PSO 策略（敏感度指导搜索提效降本）；(3) 仅 50 校准样本的轻量评估方案；(4) 多架构实验验证 PSOQ 在精度/效率/资源上持续优于 SOTA PTQ。
  引用文献：无

▸ 行文逻辑总结：从"电网缺陷检测需求"的大背景出发，梳理深度学习驱动检测 → 边缘部署痛点 → 量化压缩优势 → PTQ 数据/成本优势 → PTQ 低比特退化与层敏感性问题 → MPQ 的解决思路与其 NAS 搜索成本痛点 → 提出 PSOQ（Supernet+PSO+层重要性）——由应用动机到技术脉络到方法提出，层层聚焦、逻辑完整。

## 四、Methods 摘要

- **被试**：本文不涉及人类被试。使用 ImageNet2012 分类基准（>120 万训练/10 万测试/5 万验证，1000 类）与电力设备绝缘子缺陷检测数据集（国家电网，原 3564 张高分辨率图像，5 类：正常/破损/污染/松动/闪灼，经翻转/平移/旋转/缩放增强至约 10000 张，缩放至 150×150，60/20/20 划分）。模型含 ResNet18/50/101、SqueezeNet、ShuffleNet-V2、MobileNet-V2。
- **实验范式**：retraining-free MPQ——先训练权重共享 Supernet，再用层重要性引导 PSO 搜索最优位宽配置，最后轻量特征校准，全程仅用 50 无标签样本评估。
- **实验流程**：

1. BN 折叠入前接卷积层；权重 per-channel、激活 per-layer 非对称均匀量化，激活固定 8 位
2. Supernet 训练：Monte Carlo 采样（每迭代随机采 8 个位宽策略），Adam（lr=0.001），300 epoch；动态位宽冻结抑制低比特干扰
3. 层重要性计算：对每层量化到低位宽与高位宽的输出误差差 G_j=E_j(b_low)−E_j(b_high)
4. PSO 搜索（Algorithm 1）：粒子=位宽配置，速度更新含惯性/认知/社会/重要性四项；约束平均位宽≤b_target；用 50 样本评估适应度（量化模型与原模型输出 MSE）
5. 轻量特征校准（Algorithm 2）：teacher-student 对齐输出 logits 与中间特征，STE 更新 FP32 影子权重再重量化
6. 按最优策略量化部署

- **数据分析方法**：

量化策略评估——E(Π)=1/N·Σ(Q_Π(x_i)−M(x_i))²，用模型输出而非标签，50 样本即可可靠评估
Supernet 训练——Monte Carlo 采样近似期望损失，权重共享使 N^(2L) 配置共用一组权重
位宽干扰分析——二阶 Taylor 展开揭示低比特更新 ΔW 经 Hessian 放大扰动高比特路径
动态位宽冻结——按权重靠近量化边界的不稳定性评分 ΔŴ_unstable 选 Top-K 层冻结最低位宽，K 按余弦退火
层重要性——G_j=E_j(b_low)−E_j(b_high)，越大越敏感应配高位宽
PSO 速度更新——v=ωv+φ₁r₁(pbest−x)+φ₂r₂(gbest−x)+η·Normalize(G)，重要性作方向项
特征校准 loss——L=α·‖Q(x)−M(x)‖²+β·‖F_Q(x)−F_M(x)‖²，输出+中间特征双对齐

## 五、Results 逐一对应

[1] 分析方法：样本数影响（Table 1，MobileNet-V2 4 位）
→ 结果：50/100/200/400 样本 Top-1 分别 68.92/69.05/69.08/69.11，样本数增加仅微弱提升。
→ 结论：50 样本足够可靠评估，比完整测试集约省 2000x 计算。

[2] 分析方法：ImageNet 分类对比（Tables 2、3）
→ 结果：PSOQ 在 ResNet18/50/101（68.67/75.68/76.86）、SqueezeNet（55.64）、ShuffleNet-V2（67.01）、MobileNet-V2（68.88）上均优于 UniQ/OSME，仅 ResNet101 略低于 ACIQ（ACIQ 用非均匀通道量化更贵）；ResNet50/101 较全精度降幅<1%；MobileNet-V2 从 UniQ 的 10.12% 跃升至 68.88%。
→ 结论：PSOQ 在 sub-8-bit 尤其是紧凑网络上显著优于均匀量化，实现 7.3–7.8x 压缩、精度偏差<4%。

[3] 分析方法：缺陷检测应用（Table 4）
→ 结果：PSOQ 在绝缘子缺陷数据集上 SqueezeNet/ShuffleNet-V2/MobileNet-V2 准确率 82.66/78.64/81.48，均优于 UniQ（81.61/75.51/77.98），较全精度降幅约 2–4%。
→ 结论：PSOQ 在真实电力设备缺陷检测中有效，优于均匀量化、性能损失可接受。

[4] 分析方法：层重要性引导 PSO 消融（Table 5，Figure 6）
→ 结果：层重要性引导 PSO 较随机 PSO 收敛更快、Top-1 在 ShuffleNet-V2 提升 1.24%、MobileNet-V2 提升 1.14%。
→ 结论：层重要性引导加速搜索并提升最终配置质量。

[5] 分析方法：MPQ 与特征校准消融（Table 6）
→ 结果：均匀 4 位 UniQ 在 ShuffleNet-V2/MobileNet-V2 仅 40.18/10.11；MPQ（无校准）升至 61.73/66.43；UniQ+校准 65.86/62.17；PSOQ（MPQ+校准）达 66.34/68.77；MPQ 较均匀在 MobileNet-V2 增益 6.6%。
→ 结论：MPQ 与特征校准均贡献显著，二者结合最优。

▸ 行文逻辑总结：先验证样本数选择的合理性（50 足够），再在 ImageNet 全面对比 SOTA，随后在缺陷检测真实场景验证实用性，最后消融层重要性引导与 MPQ/校准各组件贡献——从评估设计到主结果到应用验证到消融，层层递进、证据充分。

## 六、Discussion 各段摘要与行文逻辑

【第1段 · 定位词：This study proposed a PSOQ framework】
▸ 主要内容：总结 PSOQ——通过 Supernet 架构、层重要性 PSO 搜索、Monte Carlo 采样与动态位宽冻结，用最少无标签校准样本快速确定最优量化配置；实验显示 7.3–7.8x 压缩、精度偏差<4%，优于现有 PTQ；在 sub-8-bit（多数方法显著退化处）表现尤优。

【第2段 · 定位词：Although PSOQ demonstrated strong performance】
▸ 主要内容：承认局限——2 位极低位宽时动态冻结可能未能完全抑制量化噪声致精度退化；网络加深时 PSO 搜索效率因搜索空间指数增长而下降；展望改进极低位宽冻结机制、为深网优化 PSO（剪枝搜索空间或更先进采样）。

【第3段 · 定位词：In future studies, PSOQ will be】
▸ 主要内容：展望——将 PSOQ 从权重量化扩展到激活量化实现端到端压缩；面对激活分布强动态性、噪声累积、硬件兼容、与权重量化协同等挑战，拟用自适应量化参数、层敏感量化、硬件感知设计与联合优化搜索应对；使 PSOQ 成为通用即插即用部署方案。

【第4段 · 定位词：At the hardware adaptation level】
▸ 主要内容：硬件适配展望——采用硬件感知量化策略（嵌入位宽/指令集约束生成直接可用量化方案），提供轻量工具适配边缘设备资源与实时需求。

▸ 行文逻辑总结：总结核心成果 → 承认局限（极低位宽/深网搜索效率）并给改进方向 → 展望激活量化扩展与端到端压缩 → 硬件感知适配，遵循"总结→局限→未来"的收束逻辑。

## 七、我的阅读笔记（待填写）

【核心贡献与意义】



【与我研究的关联】



【方法借鉴点】



【疑问与待深入之处】



【其他备注】

