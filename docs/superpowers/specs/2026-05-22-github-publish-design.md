# ReadPaper GitHub 发布设计文档

**日期**：2026-05-22  
**方案**：A — 两个独立 GitHub Repo，Skill 运行时路径自动探测

---

## 背景

ReadPaper 是一个学术论文批量阅读辅助工具，通过 MinerU 将 PDF 转为 Markdown，再由 AI 深度分析生成结构化 DOCX 阅读笔记。当前状态：
- 代码已在本地 git 管理，尚未推送到 GitHub
- `.claude/skills/` 下有 4 个自定义 Skill，含大量硬编码个人路径
- 缺少 README、.gitignore、requirements.txt

目标：完全开源发布，任何人可克隆使用。

---

## Repo 一：ReadPaper 项目 Repo

### 定位
包含项目核心代码、Skill 文件、文档，面向希望使用完整工具链的用户。

### 目录结构（发布后）

```
ReadPaper/
├── .claude/
│   ├── skills/
│   │   ├── 阅读并总结文献/SKILL.md          ← 路径已泛化
│   │   ├── 批量阅读并总结文献/SKILL.md       ← 路径已泛化
│   │   ├── 驱动MinerU执行PDF→MD转换/SKILL.md ← 路径已泛化
│   │   └── 在线MinerU执行PDF→MD转换/SKILL.md ← 路径已泛化
│   └── settings.local.json                  ← gitignored
├── scripts/
│   ├── generate_reading_notes.py
│   └── cors_server.py
├── docs/
│   └── superpowers/
│       ├── specs/
│       └── plans/
├── pdf_unread/.gitkeep
├── pdf_done/.gitkeep
├── md_unread/.gitkeep
├── md_done/.gitkeep
├── docx_done/.gitkeep
├── .gitignore
├── requirements.txt
├── CLAUDE.md                                 ← 已清理个人信息
└── README.md                                 ← 新增
```

### .gitignore 规则

```gitignore
# Claude Code 本地配置
.claude/settings.local.json
.claude/worktrees/

# Python 缓存
scripts/__pycache__/
scripts/_temp_analysis.json
scripts/desktop_screenshot.png
*.pyc

# 数据目录内容（目录本身保留靠 .gitkeep，内容不入库）
pdf_unread/*.pdf
pdf_done/*.pdf
md_unread/*.md
md_done/*.md
docx_done/*.docx
```

### CLAUDE.md 修改内容

1. 删除所有 `C:\Users\YingyanChen\...` 绝对路径，改为说明"以 CLAUDE.md 所在目录为项目根目录"
2. 删除"本次运行（2026-05-21）使用的 Skill"章节（会话级信息）
3. Skill 包路径表格保留，但路径改为相对路径

### requirements.txt

```
python-docx
```

### README.md 结构

1. 项目简介（一段话 + 工作流图）
2. 前置依赖（Python 3.8+、python-docx、MinerU 或 mineru.net 账号）
3. 安装步骤
4. 使用方法（4 个命令各一节）
5. Skill 安装说明（链接到 readpaper-skills repo）
6. 目录结构说明

---

## Repo 二：readpaper-skills 插件 Repo

### 定位
仅包含 4 个 Skill 文件，面向只想要 AI 技能、不需要完整项目的用户。

### 目录结构

```
readpaper-skills/
├── .claude/
│   └── skills/
│       ├── 阅读并总结文献/SKILL.md
│       ├── 批量阅读并总结文献/SKILL.md
│       ├── 驱动MinerU执行PDF→MD转换/SKILL.md
│       └── 在线MinerU执行PDF→MD转换/SKILL.md
└── README.md
```

### 安装方式（写入 README）

```powershell
# Windows PowerShell
git clone https://github.com/<username>/readpaper-skills
xcopy readpaper-skills\.claude\skills\ <your-project>\.claude\skills\ /E /I
```

```bash
# macOS / Linux（技能文件跨平台，但技能内 PowerShell 命令仅限 Windows）
git clone https://github.com/<username>/readpaper-skills
cp -r readpaper-skills/.claude/skills/ <your-project>/.claude/skills/
```

### README.md 结构

1. 简介（这是 ReadPaper 项目的配套 Skill 插件）
2. 包含技能列表（4 个命令说明）
3. 安装步骤
4. 依赖说明（Python、python-docx、MinerU）
5. 链接回主项目 repo

---

## Skill 路径泛化方案（4 个 SKILL.md 统一修改）

### 问题
当前所有 SKILL.md 硬编码了：
- `C:\Users\YingyanChen\Desktop\CC_file\ReadPaper`（项目根目录）
- `C:\Users\YingyanChen\.workbuddy\binaries\python\envs\default\Scripts\python.exe`（Python 路径）

### 解决方案：运行时自动探测

在每个 SKILL.md 的"第 1 步"前插入**路径初始化步骤**：

```
### 第 0 步：初始化运行环境

**探测项目根目录**
使用 PowerShell 获取当前工作目录：
```powershell
(Get-Location).Path
```
将输出值记为 `$PROJECT_ROOT`，用于后续所有路径拼接。

**探测 Python 路径**（仅"阅读并总结文献"和"在线MinerU"Skill 需要）
```powershell
(Get-Command python -ErrorAction SilentlyContinue).Source
```
- 若有输出：记为 `$PYTHON_EXE`
- 若无输出：提示用户"未检测到 python 命令，请确认已安装 Python 并添加到 PATH"，停止执行
```

后续所有步骤中将：
- `C:\Users\YingyanChen\Desktop\CC_file\ReadPaper` → `$PROJECT_ROOT`
- `C:\Users\YingyanChen\.workbuddy\binaries\python\envs\default\Scripts\python.exe` → `$PYTHON_EXE`
- `C:\Users\YingyanChen\.workbuddy\binaries\python\envs\default\Scripts\pip.exe` → `pip`（或 `$PYTHON_EXE -m pip`）

---

## 发布顺序

1. 整理项目 repo（清理 + 新增文件）
2. 推送主项目到 GitHub（创建 public repo）
3. 创建 readpaper-skills repo，将泛化后的 SKILL.md 复制进去
4. 推送 skills repo 到 GitHub
5. 在两个 repo 的 README 中互相添加链接

---

## 排除在外的内容

- `.claude/worktrees/`：临时工作树，完全排除
- `docs/superpowers/specs/*.md`（含本文件）：随项目一起入库，作为公开设计文档
- 用户个人数据（PDF、MD、DOCX 文件）：通过 .gitignore 排除
