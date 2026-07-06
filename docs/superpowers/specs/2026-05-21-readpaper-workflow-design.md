# ReadPaper 学术论文阅读辅助系统 — 设计文档

**日期：** 2026-05-21  
**状态：** 已批准

---

## 一、项目背景

用户是认知/神经科学领域研究者，需要批量精读英文学术论文。现有工作流：

1. PDF文件通过 **MinerU** 外部工具转换为Markdown文件
2. 本项目负责读取Markdown → AI深度分析 → 生成结构化DOCX阅读笔记 → 管理文件状态

项目目录：`C:\Users\YingyanChen\Desktop\CC_file\ReadPaper\`

---

## 二、文件夹结构与工作流

```
pdf_unread\   →  [MinerU转换]  →  pdf_done\      （PDF归档）
                               →  md_unread\  →  [Claude分析]  →  md_done\    （MD归档）
                                                               →  docx_done\  （阅读笔记）
```

| 文件夹 | 说明 |
|--------|------|
| `pdf_unread\` | 待转换的原始PDF，只读，不修改 |
| `pdf_done\` | 已通过MinerU转换完毕的PDF归档 |
| `md_unread\` | MinerU生成的MD文件，待处理（输入队列） |
| `md_done\` | 已生成阅读笔记DOCX的MD文件归档 |
| `docx_done\` | 生成的论文阅读笔记DOCX文件 |

**MD文件命名规律（MinerU生成）：**  
`MinerU_markdown_[论文标题]_[数字ID].md`

**DOCX文件命名规则：**  
`[论文标题].docx`（去掉 `MinerU_markdown_` 前缀和末尾 `_[数字ID]` 后缀）

---

## 三、Skill 列表（共3个）

### Skill 1：`驱动MinerU执行PDF→MD转换`

**触发命令：**
```
/驱动MinerU执行PDF→MD转换 [文件名] [--from 文件夹A] [--to 文件夹B]
```
- `文件名`：可选，不指定则处理来源文件夹中按字母顺序第一篇PDF
- `--from 文件夹A`：可选，PDF来源文件夹，默认 `pdf_unread\`
- `--to 文件夹B`：可选，MD输出文件夹，默认 `md_unread\`

**功能：** 调用MinerU将PDF转换为MD，并将结果保存到指定位置。

**行为：**
1. 确定来源文件夹 A（`--from` 参数 或 默认 `pdf_unread\`）
2. 在文件夹 A 中找到目标PDF文件（指定文件名 或 按字母顺序第一篇）
3. 确定MD输出文件夹 B（`--to` 参数 或 默认 `md_unread\`）
4. 调用MinerU命令行，将PDF转换为MD并直接输出到文件夹 B：
   `mineru -p "文件夹A\Aa.pdf" -o "文件夹B"`
5. 确认MD文件已生成在文件夹 B 中
6. 将原始PDF从文件夹 A 移动到 `pdf_done\`（固定归档目标，不可自定义）
7. 报告完成，告知：MD已保存到文件夹B / PDF已归档到 pdf_done\

**前置条件：** MinerU已安装并可在命令行中执行（`pip install mineru`）

---

### Skill 2：`阅读并总结文献`

**触发命令：**
```
/阅读并总结文献 [文件名] [--from 文件夹C] [--md-to 文件夹D] [--docx-to 文件夹E]
```
- `文件名`：可选，不指定则处理来源文件夹中按字母顺序第一篇MD
- `--from 文件夹C`：可选，MD来源文件夹，默认 `md_unread\`
- `--md-to 文件夹D`：可选，处理完毕后MD的归档文件夹，默认 `md_done\`
- `--docx-to 文件夹E`：可选，DOCX输出文件夹，默认 `docx_done\`

**功能：** 处理单篇论文，生成完整阅读笔记DOCX。

**行为：**
1. 确定各文件夹路径（参数 或 默认值）
2. 在来源文件夹中找到指定MD文件（或按字母顺序第一篇）
3. 读取全部MD内容
4. 按照阅读笔记结构（见第四节）逐节进行AI分析
5. 使用 python-docx 生成DOCX文件，保存到 `--docx-to` 文件夹
6. 将MD文件移动到 `--md-to` 文件夹
7. 报告完成，告知DOCX路径

---

### Skill 3：`批量阅读并总结文献`

**触发命令：**
```
/批量阅读并总结文献 [--from 文件夹C] [--md-to 文件夹D] [--docx-to 文件夹E]
```
- 三个参数与 `/阅读并总结文献` 含义相同，默认值相同

**功能：** 批量处理指定文件夹中所有MD论文。

**行为：**
1. 确定各文件夹路径（参数 或 默认值）
2. 列出来源文件夹中所有MD文件
3. 若为空：提示"没有待处理的论文"
4. 逐篇按 `read-paper` 逻辑处理（使用相同的文件夹参数）
5. 每篇完成后报告进度（第X篇/共Y篇）
6. 全部完成后汇总报告

---

## 四、阅读笔记DOCX结构

每篇论文生成一个DOCX文件，包含以下7个部分：

### 1. 关键词卡片
| 维度 | 内容 |
|------|------|
| 研究问题 | （自动提取） |
| 技术手段 | EEG / fMRI / 行为实验 / 建模 等 |
| 实验范式 | （自动提取） |
| 数据分析方法 | （自动提取） |
| 主要结论 | （自动提取） |
| 创新点 | （自动提取） |

### 2. Abstract
- Abstract原文（保留英文）
- 中文翻译

### 3. Introduction 各段摘要与行文逻辑
每段格式：
```
【第N段 · 定位词：<原文该段首句前五个词>】
▸ 主要内容：...
（如有引用关键文献，注明作者年份）
```
末尾附：
```
▸ 行文逻辑总结：（描述从大背景聚焦到具体研究问题的论述路径）
```

### 4. Methods 摘要
- 被试：人数、纳排标准（如有）
- 实验范式：简述任务设计
- 实验流程：关键步骤
- 数据分析方法：列点说明

### 5. Results 逐一对应
每条分析方法对应格式：
```
【分析方法X】→【结果】→【结论】
```
末尾附：
```
▸ 行文逻辑总结：（描述结果部分的推理路径和论述结构）
```

### 6. Discussion 各段摘要与行文逻辑
每段格式：
```
【第N段 · 定位词：<原文该段首句前五个词>】
▸ 主要内容：...
```
末尾附：
```
▸ 行文逻辑总结：（实验内容概述 → 优点 → 局限性 → 未来方向）
```

### 7. 我的阅读笔记（空白区）
```
【核心贡献与意义】


【与我研究的关联】


【方法借鉴点】


【疑问与待深入之处】


【其他备注】

```

---

## 五、技术要求

- **Python 包：** `python-docx`（安装命令：`pip install python-docx`）
- **依赖Skill：** `anthropic-skills:docx`（系统已内置，生成DOCX时自动调用）
- **Python版本：** 3.8+

---

## 六、项目文件结构（完整）

```
ReadPaper\
├── CLAUDE.md                       ← 项目配置文件
├── docs\
│   └── superpowers\
│       └── specs\
│           └── 2026-05-21-readpaper-workflow-design.md  ← 本文件
├── .claude\
│   └── skills\
│       ├── 驱动MinerU执行PDF→MD转换\
│       │   └── SKILL.md
│       ├── 阅读并总结文献\
│       │   └── SKILL.md
│       └── 批量阅读并总结文献\
│           └── SKILL.md
├── pdf_unread\
├── pdf_done\
├── md_unread\
├── md_done\
└── docx_done\
```

---

## 七、待创建内容清单

1. `CLAUDE.md` — 项目根目录
2. `.claude\skills\驱动MinerU执行PDF→MD转换\SKILL.md`
3. `.claude\skills\阅读并总结文献\SKILL.md`
4. `.claude\skills\批量阅读并总结文献\SKILL.md`
5. 创建缺失文件夹：`pdf_unread\`、`md_done\`、`docx_done\`（`pdf_done\` 和 `md_unread\` 已存在）
6. 安装依赖：`pip install python-docx mineru`
