# ReadPaper 学术论文阅读辅助系统 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在 ReadPaper 项目中创建 CLAUDE.md、三个 Skill 文件和一个 DOCX 生成脚本，实现 PDF→MD 转换驱动、MD 深度分析、结构化 DOCX 阅读笔记生成及文件自动归档的完整工作流。

**Architecture:** 三个 SKILL.md 文件定义 Claude 的行为规则；`scripts/generate_reading_notes.py` 读取 JSON 分析数据并生成 DOCX，由 Skill 2 调用；CLAUDE.md 提供项目全局上下文。所有文件夹路径支持参数覆盖，有合理默认值。

**Tech Stack:** Python 3.8+ · python-docx · MinerU (magic-pdf CLI) · Claude Code Skills (SKILL.md)

---

## 文件清单

| 操作 | 路径 | 说明 |
|------|------|------|
| 创建 | `CLAUDE.md` | 项目配置，每次启动自动读取 |
| 创建 | `scripts/generate_reading_notes.py` | DOCX 生成脚本，由 Skill 2/3 调用 |
| 创建 | `.claude/skills/驱动MinerU执行PDF→MD转换/SKILL.md` | Skill 1 指令文件 |
| 创建 | `.claude/skills/阅读并总结文献/SKILL.md` | Skill 2 指令文件 |
| 创建 | `.claude/skills/批量阅读并总结文献/SKILL.md` | Skill 3 指令文件 |
| 创建 | `pdf_unread/`、`md_done/`、`docx_done/`、`scripts/` | 缺失目录 |

---

### Task 1：环境搭建与目录创建

**Files:**
- Create dir: `pdf_unread\`
- Create dir: `md_done\`
- Create dir: `docx_done\`
- Create dir: `scripts\`
- Create dir: `.claude\skills\驱动MinerU执行PDF→MD转换\`
- Create dir: `.claude\skills\阅读并总结文献\`
- Create dir: `.claude\skills\批量阅读并总结文献\`

- [ ] **Step 1: 安装 python-docx**

```powershell
pip install python-docx
```

Expected：末尾出现 `Successfully installed python-docx-x.x.x`

- [ ] **Step 2: 验证 MinerU 可用**

```powershell
magic-pdf --version
```

Expected：显示版本号。若报错 `command not found`，执行 `pip install "magic-pdf[full]"` 后重试。

- [ ] **Step 3: 创建所有缺失目录**

```powershell
$root = "C:\Users\YingyanChen\Desktop\CC_file\ReadPaper"
@("pdf_unread","md_done","docx_done","scripts",
  ".claude\skills\驱动MinerU执行PDF→MD转换",
  ".claude\skills\阅读并总结文献",
  ".claude\skills\批量阅读并总结文献") | ForEach-Object {
  New-Item -ItemType Directory -Force -Path "$root\$_"
}
```

Expected：每行输出一个目录对象，无报错。

- [ ] **Step 4: 确认目录结构**

```powershell
Get-ChildItem "C:\Users\YingyanChen\Desktop\CC_file\ReadPaper" -Directory | Select-Object Name
```

Expected：列出 `pdf_unread`、`pdf_done`、`md_unread`、`md_done`、`docx_done`、`scripts`、`.claude`、`docs`

---

### Task 2：创建 CLAUDE.md

**Files:**
- Create: `CLAUDE.md`

- [ ] **Step 1: 写入 CLAUDE.md**

在项目根目录 `C:\Users\YingyanChen\Desktop\CC_file\ReadPaper\` 创建文件，内容如下：

```markdown
# ReadPaper 学术论文阅读辅助系统

## 项目简介
学术论文批量阅读辅助工具。通过 MinerU 将 PDF 转为 Markdown，
再由本项目 AI 深度分析，生成结构化 DOCX 阅读笔记，并管理文件状态流转。

## 文件夹结构与工作流
```
pdf_unread\ →[/驱动MinerU执行PDF→MD转换]→ pdf_done\（PDF归档）
                                         → md_unread\
md_unread\  →[/阅读并总结文献]→ md_done\（MD归档）
                              → docx_done\（阅读笔记）
```

| 文件夹 | 说明 |
|--------|------|
| `pdf_unread\` | 待转换原始 PDF，只读 |
| `pdf_done\`   | 已转换完毕 PDF 归档 |
| `md_unread\`  | MinerU 生成的 MD 文件，待处理 |
| `md_done\`    | 已生成 DOCX 的 MD 归档 |
| `docx_done\`  | 生成的论文阅读笔记 DOCX |

## 可用命令

| 命令 | 参数 | 说明 |
|------|------|------|
| `/驱动MinerU执行PDF→MD转换` | `[文件名] [--from A] [--to B]` | PDF→MD 转换，默认 A=pdf_unread B=md_unread |
| `/阅读并总结文献` | `[文件名] [--from C] [--md-to D] [--docx-to E]` | 单篇分析，默认 C=md_unread D=md_done E=docx_done |
| `/批量阅读并总结文献` | `[--from C] [--md-to D] [--docx-to E]` | 批量分析，参数同上 |

## 技术栈
- Python 3.8+ · python-docx · MinerU (magic-pdf CLI)
- DOCX 生成脚本：`scripts/generate_reading_notes.py`

## MD 文件命名规律（MinerU 生成）
`MinerU_markdown_[论文标题]_[数字ID].md`

## DOCX 文件命名规则
去掉 `MinerU_markdown_` 前缀和末尾 `_[数字ID]` 后缀，得到论文标题，加 `.docx`。
```

- [ ] **Step 2: 验证文件存在**

```powershell
Test-Path "C:\Users\YingyanChen\Desktop\CC_file\ReadPaper\CLAUDE.md"
```

Expected：`True`

---

### Task 3：创建 DOCX 生成脚本

**Files:**
- Create: `scripts\generate_reading_notes.py`

- [ ] **Step 1: 写入脚本**

创建 `C:\Users\YingyanChen\Desktop\CC_file\ReadPaper\scripts\generate_reading_notes.py`，内容如下：

```python
"""
ReadPaper DOCX 阅读笔记生成器
用法：python generate_reading_notes.py <data.json路径> <output.docx路径>
"""
import json
import sys
import os
from datetime import datetime
from docx import Document
from docx.shared import Pt


def add_labeled(doc, label, text):
    p = doc.add_paragraph()
    p.add_run(label).bold = True
    p.add_run(text)
    return p


def create_reading_notes(data_path, output_path):
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    doc = Document()

    # ── 标题 ──
    doc.add_heading('论文阅读笔记', level=0)
    doc.add_heading(data['title'], level=1)
    doc.add_paragraph(f"生成日期：{data.get('date', datetime.now().strftime('%Y-%m-%d'))}")

    # ── 一、关键词卡片 ──
    doc.add_heading('一、关键词卡片', level=2)
    table = doc.add_table(rows=7, cols=2)
    table.style = 'Table Grid'
    hdr = table.rows[0].cells
    hdr[0].text = '维度'
    hdr[1].text = '内容'
    for cell in hdr:
        cell.paragraphs[0].runs[0].bold = True
    kw = data['keywords']
    for i, (label, value) in enumerate([
        ('研究问题',     kw['research_question']),
        ('技术手段',     kw['techniques']),
        ('实验范式',     kw['paradigm']),
        ('数据分析方法', kw['analysis_methods']),
        ('主要结论',     kw['conclusions']),
        ('创新点',       kw['innovations']),
    ], start=1):
        row = table.rows[i].cells
        row[0].text = label
        row[1].text = value
    doc.add_paragraph()

    # ── 二、Abstract ──
    doc.add_heading('二、Abstract', level=2)
    doc.add_heading('原文（英文）', level=3)
    doc.add_paragraph(data['abstract_en'])
    doc.add_heading('中文翻译', level=3)
    doc.add_paragraph(data['abstract_zh'])

    # ── 三、Introduction ──
    doc.add_heading('三、Introduction 各段摘要与行文逻辑', level=2)
    for i, para in enumerate(data['intro_paragraphs'], start=1):
        doc.add_paragraph(f"【第{i}段 · 定位词：{para['locator']}】")
        add_labeled(doc, '▸ 主要内容：', para['summary'])
        if para.get('citations'):
            add_labeled(doc, '  引用文献：', para['citations'])
    doc.add_paragraph()
    add_labeled(doc, '▸ 行文逻辑总结：', data['intro_logic'])

    # ── 四、Methods ──
    doc.add_heading('四、Methods 摘要', level=2)
    m = data['methods']
    add_labeled(doc, '被试：',       m['participants'])
    add_labeled(doc, '实验范式：',   m['paradigm'])
    add_labeled(doc, '实验流程：',   m['procedure'])
    add_labeled(doc, '数据分析方法：', m['analysis'])

    # ── 五、Results ──
    doc.add_heading('五、Results 逐一对应', level=2)
    for i, item in enumerate(data['results'], start=1):
        add_labeled(doc, f'[{i}] 分析方法：', item['method'])
        add_labeled(doc, '→ 结果：',          item['result'])
        add_labeled(doc, '→ 结论：',          item['conclusion'])
        doc.add_paragraph()
    add_labeled(doc, '▸ 行文逻辑总结：', data['results_logic'])

    # ── 六、Discussion ──
    doc.add_heading('六、Discussion 各段摘要与行文逻辑', level=2)
    for i, para in enumerate(data['disc_paragraphs'], start=1):
        doc.add_paragraph(f"【第{i}段 · 定位词：{para['locator']}】")
        add_labeled(doc, '▸ 主要内容：', para['summary'])
    doc.add_paragraph()
    add_labeled(doc, '▸ 行文逻辑总结：', data['disc_logic'])

    # ── 七、我的阅读笔记 ──
    doc.add_heading('七、我的阅读笔记（待填写）', level=2)
    for name in ['核心贡献与意义', '与我研究的关联', '方法借鉴点', '疑问与待深入之处', '其他备注']:
        add_labeled(doc, f'【{name}】', '')
        doc.add_paragraph()
        doc.add_paragraph()

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    doc.save(output_path)
    print(f"✓ DOCX 已保存：{output_path}")


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("用法：python generate_reading_notes.py <data.json> <output.docx>")
        sys.exit(1)
    create_reading_notes(sys.argv[1], sys.argv[2])
```

- [ ] **Step 2: 冒烟测试脚本（用最小 JSON 验证脚本可运行）**

在 PowerShell 中执行：

```powershell
$testJson = @'
{
  "title": "Test Paper",
  "date": "2026-05-21",
  "keywords": {"research_question":"Q","techniques":"fMRI","paradigm":"P","analysis_methods":"GLM","conclusions":"C","innovations":"I"},
  "abstract_en": "English abstract.",
  "abstract_zh": "中文摘要。",
  "intro_paragraphs": [{"locator":"First five words here","summary":"段落摘要","citations":"Smith, 2020"}],
  "intro_logic": "行文逻辑。",
  "methods": {"participants":"N=20","paradigm":"范式","procedure":"步骤","analysis":"GLM"},
  "results": [{"method":"GLM","result":"p<.05","conclusion":"显著"}],
  "results_logic": "逻辑。",
  "disc_paragraphs": [{"locator":"First five discussion words","summary":"讨论摘要"}],
  "disc_logic": "讨论逻辑。"
}
'@
$testJson | Out-File -Encoding utf8 "C:\Users\YingyanChen\Desktop\CC_file\ReadPaper\scripts\_test.json"
python "C:\Users\YingyanChen\Desktop\CC_file\ReadPaper\scripts\generate_reading_notes.py" `
  "C:\Users\YingyanChen\Desktop\CC_file\ReadPaper\scripts\_test.json" `
  "C:\Users\YingyanChen\Desktop\CC_file\ReadPaper\scripts\_test_output.docx"
```

Expected：输出 `✓ DOCX 已保存：...\_test_output.docx`，文件存在。

- [ ] **Step 3: 清理测试文件**

```powershell
Remove-Item "C:\Users\YingyanChen\Desktop\CC_file\ReadPaper\scripts\_test.json"
Remove-Item "C:\Users\YingyanChen\Desktop\CC_file\ReadPaper\scripts\_test_output.docx"
```

Expected：两个文件被删除，无报错。

---

### Task 4：创建 Skill 1 — 驱动MinerU执行PDF→MD转换

**Files:**
- Create: `.claude\skills\驱动MinerU执行PDF→MD转换\SKILL.md`

- [ ] **Step 1: 写入 SKILL.md**

创建 `C:\Users\YingyanChen\Desktop\CC_file\ReadPaper\.claude\skills\驱动MinerU执行PDF→MD转换\SKILL.md`，内容如下：

````markdown
# 驱动MinerU执行PDF→MD转换

当用户输入 `/驱动MinerU执行PDF→MD转换` 时，严格按以下步骤执行。

## 项目根目录
`C:\Users\YingyanChen\Desktop\CC_file\ReadPaper`

## 参数解析

从用户消息中提取以下参数（均为可选）：

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `文件名` | 目标 PDF 文件名（可带或不带 `.pdf`） | 来源文件夹中字母顺序第一篇 |
| `--from 路径` | PDF 来源文件夹（绝对路径或相对于项目根目录） | `pdf_unread` |
| `--to 路径` | MD 输出文件夹（绝对路径或相对于项目根目录） | `md_unread` |

PDF 归档目标（固定，不可修改）：项目根目录下的 `pdf_done`

## 执行步骤

### 第 1 步：确定完整路径

- 来源文件夹 A = `--from` 值（若为相对路径则拼接项目根目录）或 `C:\Users\YingyanChen\Desktop\CC_file\ReadPaper\pdf_unread`
- 输出文件夹 B = `--to` 值（若为相对路径则拼接项目根目录）或 `C:\Users\YingyanChen\Desktop\CC_file\ReadPaper\md_unread`
- PDF 归档目标 = `C:\Users\YingyanChen\Desktop\CC_file\ReadPaper\pdf_done`

### 第 2 步：找到目标 PDF

使用 Glob 工具列出文件夹 A 中所有 `.pdf` 文件：

- 若用户指定了文件名：找到匹配文件（自动补全 `.pdf` 后缀）
- 若未指定：取字母顺序第一个 `.pdf` 文件
- 若文件夹 A 中没有 PDF：告知用户 "【文件夹A】中没有找到 PDF 文件"，停止执行

### 第 3 步：创建临时输出目录

在文件夹 B 下创建临时目录 `_mineru_temp`：
`【文件夹B】\_mineru_temp`

### 第 4 步：调用 MinerU 执行转换

使用 Bash 工具执行：

```bash
magic-pdf -p "【PDF完整路径】" -o "【文件夹B】\_mineru_temp" -m auto
```

等待命令完成。若报错 `magic-pdf: command not found`，改用：

```bash
mineru -p "【PDF完整路径】" -o "【文件夹B】\_mineru_temp" -m auto
```

若仍报错，告知用户 "MinerU 未安装，请执行：`pip install magic-pdf[full]`"，停止执行。

### 第 5 步：将 MD 文件移到文件夹 B

MinerU 在临时目录下生成子目录结构。使用 Glob 工具递归查找 `_mineru_temp` 下的所有 `.md` 文件：

```
【文件夹B】\_mineru_temp\**\*.md
```

将找到的每个 `.md` 文件移动到文件夹 B 根目录（仅移动文件，不保留子目录结构）。

### 第 6 步：删除临时目录

使用 Bash 工具删除 `_mineru_temp` 目录及其全部内容：

```bash
rm -rf "【文件夹B】/_mineru_temp"
```

### 第 7 步：归档原始 PDF

将 PDF 文件从文件夹 A 移动到 PDF 归档目标（`pdf_done`）。

### 第 8 步：报告结果

向用户输出：

```
✓ 已转换：【PDF文件名】
✓ MD 文件保存至：【MD文件完整路径】
✓ 原始 PDF 已归档至：pdf_done\【PDF文件名】
```
````

- [ ] **Step 2: 验证文件存在**

```powershell
Test-Path "C:\Users\YingyanChen\Desktop\CC_file\ReadPaper\.claude\skills\驱动MinerU执行PDF→MD转换\SKILL.md"
```

Expected：`True`

---

### Task 5：创建 Skill 2 — 阅读并总结文献

**Files:**
- Create: `.claude\skills\阅读并总结文献\SKILL.md`

- [ ] **Step 1: 写入 SKILL.md**

创建 `C:\Users\YingyanChen\Desktop\CC_file\ReadPaper\.claude\skills\阅读并总结文献\SKILL.md`，内容如下：

````markdown
# 阅读并总结文献

当用户输入 `/阅读并总结文献` 时，严格按以下步骤执行。

## 项目根目录
`C:\Users\YingyanChen\Desktop\CC_file\ReadPaper`

## 参数解析

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `文件名` | 目标 MD 文件名 | 来源文件夹中字母顺序第一篇 |
| `--from 路径` | MD 来源文件夹 | `md_unread` |
| `--md-to 路径` | 处理完成后 MD 的归档文件夹 | `md_done` |
| `--docx-to 路径` | DOCX 输出文件夹 | `docx_done` |

相对路径均相对于项目根目录。

## 执行步骤

### 第 1 步：确定路径

- 来源文件夹 C = `--from` 值 或 `C:\Users\YingyanChen\Desktop\CC_file\ReadPaper\md_unread`
- MD 归档文件夹 D = `--md-to` 值 或 `C:\Users\YingyanChen\Desktop\CC_file\ReadPaper\md_done`
- DOCX 输出文件夹 E = `--docx-to` 值 或 `C:\Users\YingyanChen\Desktop\CC_file\ReadPaper\docx_done`

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
→ DOCX 文件名：`Brain Bases for Navigating Acoustic Features.docx`

### 第 4 步：读取 MD 文件全部内容

使用 Read 工具读取该 MD 文件的完整内容。

### 第 5 步：AI 深度分析

对读取的 MD 内容逐节进行分析，按以下模板提取数据。**分析过程不输出到对话中，直接进入第 6 步写 JSON。**

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

### 第 6 步：将分析结果写入临时 JSON 文件

使用 Write 工具将以上分析结果写入：
`C:\Users\YingyanChen\Desktop\CC_file\ReadPaper\scripts\_temp_analysis.json`

格式如下（所有字段必须填写，不留空）：

```json
{
  "title": "论文标题",
  "date": "YYYY-MM-DD",
  "keywords": {
    "research_question": "...",
    "techniques": "...",
    "paradigm": "...",
    "analysis_methods": "...",
    "conclusions": "...",
    "innovations": "..."
  },
  "abstract_en": "完整英文 abstract...",
  "abstract_zh": "中文翻译...",
  "intro_paragraphs": [
    {"locator": "前五个单词", "summary": "段落摘要", "citations": "Smith, 2020; Jones, 2019"},
    {"locator": "...", "summary": "...", "citations": ""}
  ],
  "intro_logic": "行文逻辑总结...",
  "methods": {
    "participants": "N=20, 10男10女, 年龄18-35岁",
    "paradigm": "...",
    "procedure": "1. ...\n2. ...\n3. ...",
    "analysis": "1. GLM\n2. ROI分析\n3. ..."
  },
  "results": [
    {"method": "GLM", "result": "双侧海马激活显著增强（p<.001）", "conclusion": "海马参与非空间导航"},
    {"method": "...", "result": "...", "conclusion": "..."}
  ],
  "results_logic": "行文逻辑总结...",
  "disc_paragraphs": [
    {"locator": "The present study investigated", "summary": "段落摘要"},
    {"locator": "...", "summary": "..."}
  ],
  "disc_logic": "行文逻辑总结..."
}
```

### 第 7 步：运行 DOCX 生成脚本

使用 Bash 工具执行：

```bash
python "C:\Users\YingyanChen\Desktop\CC_file\ReadPaper\scripts\generate_reading_notes.py" "C:\Users\YingyanChen\Desktop\CC_file\ReadPaper\scripts\_temp_analysis.json" "【文件夹E完整路径】\【论文标题】.docx"
```

Expected 输出：`✓ DOCX 已保存：...`

若报错 `ModuleNotFoundError: No module named 'docx'`，先执行 `pip install python-docx` 再重试。

### 第 8 步：清理临时 JSON 文件

使用 Bash 工具删除临时文件：

```bash
rm "C:\Users\YingyanChen\Desktop\CC_file\ReadPaper\scripts\_temp_analysis.json"
```

### 第 9 步：归档 MD 文件

将 MD 文件从文件夹 C 移动到文件夹 D。

### 第 10 步：报告结果

向用户输出：

```
✓ 已处理：【MD文件名】
✓ 阅读笔记已保存至：【DOCX完整路径】
✓ MD 文件已归档至：【文件夹D路径】
```
````

- [ ] **Step 2: 验证文件存在**

```powershell
Test-Path "C:\Users\YingyanChen\Desktop\CC_file\ReadPaper\.claude\skills\阅读并总结文献\SKILL.md"
```

Expected：`True`

---

### Task 6：创建 Skill 3 — 批量阅读并总结文献

**Files:**
- Create: `.claude\skills\批量阅读并总结文献\SKILL.md`

- [ ] **Step 1: 写入 SKILL.md**

创建 `C:\Users\YingyanChen\Desktop\CC_file\ReadPaper\.claude\skills\批量阅读并总结文献\SKILL.md`，内容如下：

````markdown
# 批量阅读并总结文献

当用户输入 `/批量阅读并总结文献` 时，严格按以下步骤执行。

## 项目根目录
`C:\Users\YingyanChen\Desktop\CC_file\ReadPaper`

## 参数解析

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--from 路径` | MD 来源文件夹 | `md_unread` |
| `--md-to 路径` | 处理完成后 MD 的归档文件夹 | `md_done` |
| `--docx-to 路径` | DOCX 输出文件夹 | `docx_done` |

相对路径均相对于项目根目录。

## 执行步骤

### 第 1 步：确定路径

同 `/阅读并总结文献`：确定文件夹 C、D、E 的完整路径。

### 第 2 步：列出所有待处理 MD 文件

使用 Glob 工具列出文件夹 C 中所有 `.md` 文件，按字母顺序排列。

若没有 MD 文件：告知用户 "【文件夹C】中没有待处理的 MD 文件"，停止执行。

若有文件：告知用户 "找到 X 篇待处理文献，开始逐篇处理..."

### 第 3 步：逐篇处理

对每一篇 MD 文件，完整执行 `/阅读并总结文献` 的 **第 3 步到第 10 步**（提取标题、分析、生成DOCX、归档）。

每篇完成后立即输出进度：

```
[X/Y] ✓ 已完成：【论文标题】→ 【DOCX路径】
```

若某篇处理中出现错误，输出：

```
[X/Y] ✗ 处理失败：【MD文件名】
错误信息：【错误详情】
```

继续处理下一篇，不中断整体流程。

### 第 4 步：汇总报告

所有论文处理完成后，输出：

```
══════════════════════════════
批量处理完成
  成功：X 篇
  失败：Y 篇（若有，列出文件名）
  DOCX 保存在：【文件夹E路径】
  MD  归档在：【文件夹D路径】
══════════════════════════════
```
````

- [ ] **Step 2: 验证文件存在**

```powershell
Test-Path "C:\Users\YingyanChen\Desktop\CC_file\ReadPaper\.claude\skills\批量阅读并总结文献\SKILL.md"
```

Expected：`True`

---

### Task 7：端对端冒烟测试

**Files:**（无新增文件，测试已有 MD 文件）

- [ ] **Step 1: 确认测试素材存在**

```powershell
Get-ChildItem "C:\Users\YingyanChen\Desktop\CC_file\ReadPaper\md_unread" -Filter "*.md" |
  Select-Object -First 1 -ExpandProperty Name
```

Expected：显示一个 `MinerU_markdown_*.md` 文件名。

- [ ] **Step 2: 触发 Skill 2 处理第一篇论文**

在 Claude Code 中执行：

```
/阅读并总结文献
```

Expected：Claude 自动选取 `md_unread` 中字母顺序第一篇，完成分析后输出：
```
✓ 已处理：MinerU_markdown_A...md
✓ 阅读笔记已保存至：...docx_done\【论文标题】.docx
✓ MD 文件已归档至：...md_done\
```

- [ ] **Step 3: 确认 DOCX 文件生成**

```powershell
Get-ChildItem "C:\Users\YingyanChen\Desktop\CC_file\ReadPaper\docx_done" -Filter "*.docx"
```

Expected：列出至少一个 `.docx` 文件，文件名为论文标题。

- [ ] **Step 4: 确认 MD 文件已归档**

```powershell
Get-ChildItem "C:\Users\YingyanChen\Desktop\CC_file\ReadPaper\md_done" -Filter "*.md" |
  Select-Object Name
```

Expected：列出刚才处理的那篇 MD 文件，说明移动成功。

- [ ] **Step 5: 打开 DOCX 确认结构完整**

```powershell
Start-Process "C:\Users\YingyanChen\Desktop\CC_file\ReadPaper\docx_done\$(
  Get-ChildItem 'C:\Users\YingyanChen\Desktop\CC_file\ReadPaper\docx_done' -Filter '*.docx' |
  Select-Object -First 1 -ExpandProperty Name)"
```

Expected：Word 打开文档，目测确认包含：关键词卡片表格、Abstract原文+翻译、Introduction各段+定位词、Methods、Results逐条、Discussion各段+定位词、空白阅读笔记区。
