# 阅读并总结文献

当用户输入 `/阅读并总结文献` 时，严格按以下步骤执行。

## 项目根目录

Claude Code 启动时已自动切换至项目根目录（即包含 `CLAUDE.md` 的目录）。
后续所有相对路径均以此为基础。

## 参数解析

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `文件名` | 目标 MD 文件名 | 来源文件夹中字母顺序第一篇 |
| `--from 路径` | MD 来源文件夹 | `md_unread` |
| `--md-to 路径` | 处理完成后 MD 的归档文件夹 | `md_done` |
| `--docx-to 路径` | MD 阅读笔记输出文件夹（沿用历史参数名，实际输出 `.md`） | `docx_done` |

相对路径均相对于项目根目录。

## 执行步骤

### 第 1 步：确定路径

- 来源文件夹 C = `--from` 值 或 当前目录下的 `md_unread`
- MD 归档文件夹 D = `--md-to` 值 或 当前目录下的 `md_done`
- 笔记输出文件夹 E = `--docx-to` 值 或 当前目录下的 `docx_done`

### 第 2 步：找到目标 MD 文件

使用 Glob 工具列出文件夹 C 中所有 `.md` 文件：

- 若用户指定了文件名：找到匹配文件
- 若未指定：取字母顺序第一个 `.md` 文件
- 若没有 MD 文件：告知用户 "【文件夹C】中没有待处理的 MD 文件"，停止执行

### 第 3 步：提取论文标题

从 MD 文件名中提取论文标题：

1. 去掉 `MinerU_markdown_` 前缀
2. 去掉末尾的 `_纯数字串`（如 `_2057288022778179584`）
3. 去掉 `.md` 后缀
4. 将下划线 `_` 替换为空格

示例：`MinerU_markdown_Brain_Bases_for_Navigating_Acoustic_Features_2057288022778179584.md`
→ 论文标题：`Brain Bases for Navigating Acoustic Features`
→ 笔记文件名：`Brain Bases for Navigating Acoustic Features.md`

### 第 4 步：读取 MD 文件全部内容

使用 Read 工具读取该 MD 文件的完整内容。

### 第 5 步：AI 深度分析

对读取的 MD 内容逐节进行分析，按以下模板提取数据。**分析过程不输出到对话中，直接进入第 6 步生成 Markdown 笔记。**

---

**[A] 关键词卡片**（每项 1–3 句话，简洁）

- `research_question`：这篇论文研究什么核心问题？
- `techniques`：使用了哪些技术（EEG / fMRI / 行为实验 / 计算建模 / 眼动等）？
- `paradigm`：使用了什么实验范式？
- `analysis_methods`：主要数据分析方法有哪些（逗号分隔）？
- `conclusions`：最重要的 1–2 个结论？
- `innovations`：相比已有研究的主要创新点？

---

**[B] Abstract**

- `abstract_en`：提取 MD 中 `# Abstract` 部分的完整原文（英文，去掉页眉页脚噪声）
- `abstract_zh`：将 abstract_en 翻译为中文（保持学术语言风格）

---

**[C] Introduction 各段摘要**

找到 MD 中 `# Introduction` 部分，以空行为段落分隔，逐段处理：

对每一段生成一个对象：
- `locator`：该段正文首句的前 5 个单词（原文照录，用于定位）
- `summary`：1–3 句话概括该段核心论点
- `citations`：若该段引用了重要文献，列出"第一作者姓, 年份"；无引用则填空字符串

最后生成：
- `intro_logic`：总结 Introduction 的行文逻辑（从大背景如何逐步聚焦到具体研究问题）

---

**[D] Methods 摘要**

找到 MD 中 `# Methods` 或 `# Methods and Materials` 部分，提取：

- `participants`：被试人数（N=?）、性别比例（若有）、年龄范围（若有）、纳排标准（若有）
- `paradigm`：任务核心设计（1–3 句话）
- `procedure`：实验关键步骤（用换行分隔的多步，如"1. ...\n2. ...\n3. ..."）
- `analysis`：逐点列出所有数据分析方法（用换行分隔）

---

**[E] Results 逐一对应**

找到 MD 中 `# Results` 部分，对每个分析方法生成一个对象：
- `method`：分析方法名称（与 [D] 中对应）
- `result`：该分析的主要结果（数据、效应值等）
- `conclusion`：该结果支持的结论（作者解读）

最后生成：
- `results_logic`：总结 Results 部分的推进逻辑（各分析之间的关系与推理路径）

---

**[F] Discussion 各段摘要**

找到 MD 中 `# Discussion` 部分，以空行为段落分隔，逐段处理：

对每一段生成一个对象：
- `locator`：该段正文首句的前 5 个单词（原文照录）
- `summary`：1–3 句话概括该段主要内容

最后生成：
- `disc_logic`：总结 Discussion 的行文逻辑（通常：概述发现 → 解释结果 → 与前人比较 → 局限 → 未来方向）

---

### 第 6 步：生成 Markdown 阅读笔记

使用 Write 工具直接生成阅读笔记 Markdown 文件，保存至：
`【文件夹E完整路径】/【论文标题】.md`

**所有字段必须填写，不留空。** 按以下模板生成（将 `{{...}}` 占位符替换为第 5 步分析结果；Introduction / Results / Discussion 的条目按实际段落数量展开）：

```markdown
# 论文阅读笔记

## {{title}}

生成日期：{{date}}

## 一、关键词卡片

| 维度 | 内容 |
|------|------|
| 研究问题 | {{research_question}} |
| 技术手段 | {{techniques}} |
| 实验范式 | {{paradigm}} |
| 数据分析方法 | {{analysis_methods}} |
| 主要结论 | {{conclusions}} |
| 创新点 | {{innovations}} |

## 二、Abstract

### 原文（英文）

{{abstract_en}}

### 中文翻译

{{abstract_zh}}

## 三、Introduction 各段摘要与行文逻辑

【第1段 · 定位词：{{locator_1}}】
▸ 主要内容：{{summary_1}}
  引用文献：{{citations_1}}

【第2段 · 定位词：{{locator_2}}】
▸ 主要内容：{{summary_2}}
  引用文献：{{citations_2}}

<!-- 按实际段落数继续 -->

▸ 行文逻辑总结：{{intro_logic}}

## 四、Methods 摘要

- **被试**：{{participants}}
- **实验范式**：{{paradigm}}
- **实验流程**：

{{procedure}}

- **数据分析方法**：

{{analysis}}

## 五、Results 逐一对应

[1] 分析方法：{{method_1}}
→ 结果：{{result_1}}
→ 结论：{{conclusion_1}}

[2] 分析方法：{{method_2}}
→ 结果：{{result_2}}
→ 结论：{{conclusion_2}}

<!-- 按实际条目数继续 -->

▸ 行文逻辑总结：{{results_logic}}

## 六、Discussion 各段摘要与行文逻辑

【第1段 · 定位词：{{locator_1}}】
▸ 主要内容：{{summary_1}}

【第2段 · 定位词：{{locator_2}}】
▸ 主要内容：{{summary_2}}

<!-- 按实际段落数继续 -->

▸ 行文逻辑总结：{{disc_logic}}

## 七、我的阅读笔记（待填写）

【核心贡献与意义】



【与我研究的关联】



【方法借鉴点】



【疑问与待深入之处】



【其他备注】

```

写入成功后，确认文件已生成。

### 第 7 步：归档 MD 文件

将 MD 文件从文件夹 C 移动到文件夹 D。

### 第 8 步：报告结果

向用户输出：

```
✓ 已处理：【MD文件名】
✓ 阅读笔记已保存至：【笔记MD完整路径】
✓ MD 文件已归档至：【文件夹D路径】
```
