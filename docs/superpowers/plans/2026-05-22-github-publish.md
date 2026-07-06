# ReadPaper GitHub 发布 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将 ReadPaper 项目和 4 个配套 Skill 整理为任何人可直接克隆运行的开源状态，并准备好独立 Skill 插件 repo 所需的全部文件。

**Architecture:**
- **主项目 repo**（当前目录）：保留 skills、scripts、docs，新增 .gitignore / requirements.txt / README.md，更新 CLAUDE.md，为 5 个数据目录创建 .gitkeep。
- **Skill 插件 repo**（创建于 `../readpaper-skills/`）：4 个泛化后的 SKILL.md + 独立 README.md，用户 clone 后将 `.claude/skills/` 复制到任意项目即可使用。
- **路径泛化策略**：所有 SKILL.md 中的个人绝对路径改为 `(Get-Location).Path`（PowerShell）或 `$(pwd)`（Bash）动态获取，Python 路径改为系统 `python`。

**Tech Stack:** Markdown · PowerShell · Python 3.8+ · python-docx · MinerU CLI / mineru.net

---

## 文件映射

| 操作 | 文件 |
|------|------|
| 修改 | `CLAUDE.md` |
| 创建 | `.gitignore` |
| 创建 | `requirements.txt` |
| 创建 | `pdf_unread/.gitkeep`、`pdf_done/.gitkeep`、`md_unread/.gitkeep`、`md_done/.gitkeep`、`docx_done/.gitkeep` |
| 修改 | `.claude/skills/阅读并总结文献/SKILL.md` |
| 修改 | `.claude/skills/批量阅读并总结文献/SKILL.md` |
| 修改 | `.claude/skills/驱动MinerU执行PDF→MD转换/SKILL.md` |
| 修改 | `.claude/skills/在线MinerU执行PDF→MD转换/SKILL.md` |
| 创建 | `README.md` |
| 创建 | `../readpaper-skills/.claude/skills/` 下 4 个 SKILL.md（同主项目泛化版） |
| 创建 | `../readpaper-skills/README.md` |

---

## Task 1: 更新 CLAUDE.md

**Files:**
- Modify: `CLAUDE.md`

- [ ] **Step 1: 在文件顶部插入版权水印**

  在第 1 行前插入：

  ```markdown
  <!--
    Этот проект создан YingyanChen. Коммерческое использование запрещено.
    该项目由YingyanChen生成，禁止商用。
    This project was created by YingyanChen. Commercial use is prohibited.
  -->
  
  ```

- [ ] **Step 2: 删除会话级"本次运行"章节**

  删除以下整块内容（约 6 行）：

  ```
  ### 本次运行（2026-05-21）使用的 Skill
  | Skill | 说明 |
  |-------|------|
  | `superpowers:brainstorming` | 需求探索与设计 |
  | `superpowers:writing-plans` | 实施计划编写 |
  | `superpowers:subagent-driven-development` | 按计划逐任务派发子 Agent 执行 |
  | `/在线MinerU执行PDF→MD转换` | 批量 PDF→MD 转换（9 篇，全部完成） |
  ```

- [ ] **Step 3: 验证**

  确认文件顶部有版权注释，"本次运行"章节已消失，其余内容完整。

- [ ] **Step 4: Commit**

  ```powershell
  git add CLAUDE.md
  git commit -m "docs(CLAUDE.md): add copyright watermark, remove session-specific section"
  ```

---

## Task 2: 创建 .gitignore

**Files:**
- Create: `.gitignore`

- [ ] **Step 1: 写入 .gitignore**

  ```gitignore
  # Claude Code 本地配置与临时工作树
  .claude/settings.local.json
  .claude/worktrees/

  # Python 缓存与临时文件
  __pycache__/
  *.pyc
  scripts/_temp_analysis.json
  scripts/desktop_screenshot.png

  # 数据目录内容（目录本身由 .gitkeep 保留）
  pdf_unread/*.pdf
  pdf_done/*.pdf
  md_unread/*.md
  md_done/*.md
  docx_done/*.docx
  ```

- [ ] **Step 2: Commit**

  ```powershell
  git add .gitignore
  git commit -m "chore: add .gitignore for data files and local config"
  ```

---

## Task 3: 创建 requirements.txt 和 .gitkeep 占位文件

**Files:**
- Create: `requirements.txt`
- Create: 5 个 `.gitkeep`

- [ ] **Step 1: 写入 requirements.txt**

  ```
  python-docx>=0.8.11
  ```

- [ ] **Step 2: 创建各数据目录的 .gitkeep**

  在以下路径各创建空文件 `.gitkeep`（若目录不存在先创建目录）：
  - `pdf_unread/.gitkeep`
  - `pdf_done/.gitkeep`
  - `md_unread/.gitkeep`
  - `md_done/.gitkeep`
  - `docx_done/.gitkeep`

- [ ] **Step 3: Commit**

  ```powershell
  git add requirements.txt pdf_unread/.gitkeep pdf_done/.gitkeep md_unread/.gitkeep md_done/.gitkeep docx_done/.gitkeep
  git commit -m "chore: add requirements.txt and .gitkeep for data directories"
  ```

---

## Task 4: 泛化 `阅读并总结文献/SKILL.md`

**Files:**
- Modify: `.claude/skills/阅读并总结文献/SKILL.md`

**变更说明：** 去掉项目根目录的绝对路径，改为"当前工作目录"；Python 路径改为系统 `python`；所有 Bash 命令使用相对路径。

- [ ] **Step 1: 替换"## 项目根目录"节**

  将：
  ```
  ## 项目根目录
  `C:\Users\YingyanChen\Desktop\CC_file\ReadPaper`
  ```
  替换为：
  ```
  ## 项目根目录

  Claude Code 启动时已自动切换至项目根目录（即包含 `CLAUDE.md` 的目录）。
  后续所有相对路径均以此为基础。
  ```

- [ ] **Step 2: 替换"第 1 步"中的默认路径**

  将三处绝对路径默认值替换为相对路径表述：

  ```
  - 来源文件夹 C = `--from` 值 或 当前目录下的 `md_unread`
  - MD 归档文件夹 D = `--md-to` 值 或 当前目录下的 `md_done`
  - DOCX 输出文件夹 E = `--docx-to` 值 或 当前目录下的 `docx_done`
  ```

- [ ] **Step 3: 替换"第 6 步"中的 JSON 临时文件路径**

  将：
  ```
  `C:\Users\YingyanChen\Desktop\CC_file\ReadPaper\scripts\_temp_analysis.json`
  ```
  替换为：
  ```
  `scripts/_temp_analysis.json`（相对于项目根目录）
  ```

- [ ] **Step 4: 替换"第 7 步"中的 Python 与脚本路径**

  将 Bash 命令：
  ```bash
  "C:\Users\YingyanChen\.workbuddy\binaries\python\envs\default\Scripts\python.exe" "C:\Users\YingyanChen\Desktop\CC_file\ReadPaper\scripts\generate_reading_notes.py" "C:\Users\YingyanChen\Desktop\CC_file\ReadPaper\scripts\_temp_analysis.json" "【文件夹E完整路径】\【论文标题】.docx"
  ```
  替换为：
  ```bash
  python "scripts/generate_reading_notes.py" "scripts/_temp_analysis.json" "【文件夹E完整路径】/【论文标题】.docx"
  ```

  将 pip 安装命令：
  ```bash
  "C:\Users\YingyanChen\.workbuddy\binaries\python\envs\default\Scripts\pip.exe" install python-docx
  ```
  替换为：
  ```bash
  python -m pip install python-docx
  ```

- [ ] **Step 5: 替换"第 8 步"中的 JSON 路径**

  将：
  ```bash
  rm "C:\Users\YingyanChen\Desktop\CC_file\ReadPaper\scripts\_temp_analysis.json"
  ```
  替换为：
  ```bash
  rm "scripts/_temp_analysis.json"
  ```

- [ ] **Step 6: Commit**

  ```powershell
  git add ".claude/skills/阅读并总结文献/SKILL.md"
  git commit -m "skill(阅读并总结文献): replace hardcoded paths with relative/system paths"
  ```

---

## Task 5: 泛化 `批量阅读并总结文献/SKILL.md`

**Files:**
- Modify: `.claude/skills/批量阅读并总结文献/SKILL.md`

- [ ] **Step 1: 替换"## 项目根目录"节**

  将：
  ```
  ## 项目根目录
  `C:\Users\YingyanChen\Desktop\CC_file\ReadPaper`
  ```
  替换为：
  ```
  ## 项目根目录

  Claude Code 启动时已自动切换至项目根目录（即包含 `CLAUDE.md` 的目录）。
  后续所有相对路径均以此为基础。
  ```

- [ ] **Step 2: 替换"第 1 步"中的默认路径**

  将三处绝对路径默认值替换为：
  ```
  - 来源文件夹 C = `--from` 值 或 当前目录下的 `md_unread`
  - MD 归档文件夹 D = `--md-to` 值 或 当前目录下的 `md_done`
  - DOCX 输出文件夹 E = `--docx-to` 值 或 当前目录下的 `docx_done`
  ```

- [ ] **Step 3: Commit**

  ```powershell
  git add ".claude/skills/批量阅读并总结文献/SKILL.md"
  git commit -m "skill(批量阅读并总结文献): replace hardcoded paths with relative paths"
  ```

---

## Task 6: 泛化 `驱动MinerU执行PDF→MD转换/SKILL.md`

**Files:**
- Modify: `.claude/skills/驱动MinerU执行PDF→MD转换/SKILL.md`

- [ ] **Step 1: 替换"## 项目根目录"节**

  同 Task 4 Step 1，替换为"当前工作目录"描述。

- [ ] **Step 2: 替换"第 1 步"中的默认路径**

  将：
  ```
  - 来源文件夹 A = `--from` 值（若为相对路径则拼接项目根目录）或 `C:\Users\YingyanChen\Desktop\CC_file\ReadPaper\pdf_unread`
  - 输出文件夹 B = `--to` 值（若为相对路径则拼接项目根目录）或 `C:\Users\YingyanChen\Desktop\CC_file\ReadPaper\md_unread`
  - PDF 归档目标 = `C:\Users\YingyanChen\Desktop\CC_file\ReadPaper\pdf_done`
  ```
  替换为：
  ```
  - 来源文件夹 A = `--from` 值 或 当前目录下的 `pdf_unread`
  - 输出文件夹 B = `--to` 值 或 当前目录下的 `md_unread`
  - PDF 归档目标 = 当前目录下的 `pdf_done`
  ```

- [ ] **Step 3: Commit**

  ```powershell
  git add ".claude/skills/驱动MinerU执行PDF→MD转换/SKILL.md"
  git commit -m "skill(驱动MinerU): replace hardcoded paths with relative paths"
  ```

---

## Task 7: 泛化 `在线MinerU执行PDF→MD转换/SKILL.md`

**Files:**
- Modify: `.claude/skills/在线MinerU执行PDF→MD转换/SKILL.md`

- [ ] **Step 1: 替换"## 项目根目录"节**

  同 Task 4 Step 1。

- [ ] **Step 2: 替换"第 1 步"中的默认路径**

  将三处绝对路径默认值替换为：
  ```
  - 来源文件夹 A = `--from` 值 或 当前目录下的 `pdf_unread`
  - 输出文件夹 B = `--to` 值 或 当前目录下的 `md_unread`
  - PDF 归档目标 = 当前目录下的 `pdf_done`
  ```

- [ ] **Step 3: 替换"第 6 步"中的 CORS 服务器启动脚本**

  将：
  ```powershell
  $pdfFolder = "C:\Users\YingyanChen\Desktop\CC_file\ReadPaper\pdf_unread"
  $pyExe = "C:\Users\YingyanChen\.workbuddy\binaries\python\envs\default\Scripts\python.exe"
  $corsScript = "C:\Users\YingyanChen\Desktop\CC_file\ReadPaper\scripts\cors_server.py"
  $procId = (Start-Process -FilePath $pyExe -ArgumentList "$corsScript","$pdfFolder" -WindowStyle Hidden -PassThru).Id
  Start-Sleep -Seconds 1
  Write-Output "CORS server started (PID: $procId)"
  ```
  替换为：
  ```powershell
  $root = (Get-Location).Path
  $pdfFolder = "$root\pdf_unread"
  $pyExe = (Get-Command python -ErrorAction Stop).Source
  $corsScript = "$root\scripts\cors_server.py"
  $procId = (Start-Process -FilePath $pyExe -ArgumentList "$corsScript","$pdfFolder" -WindowStyle Hidden -PassThru).Id
  Start-Sleep -Seconds 1
  Write-Output "CORS server started (PID: $procId)"
  ```

- [ ] **Step 4: 替换"第 10 步"中的 PDF 归档路径**

  将：
  ```powershell
  Move-Item "【当前PDF完整路径】" "C:\Users\YingyanChen\Desktop\CC_file\ReadPaper\pdf_done\【当前PDF文件名】" -Force
  ```
  替换为：
  ```powershell
  $root = (Get-Location).Path
  Move-Item "【当前PDF完整路径】" "$root\pdf_done\【当前PDF文件名】" -Force
  ```

- [ ] **Step 5: Commit**

  ```powershell
  git add ".claude/skills/在线MinerU执行PDF→MD转换/SKILL.md"
  git commit -m "skill(在线MinerU): replace hardcoded paths with dynamic detection"
  ```

---

## Task 8: 创建项目 README.md

**Files:**
- Create: `README.md`

- [ ] **Step 1: 写入完整 README.md**

  文件内容如下（以下为完整内容，直接写入）：

  ```markdown
  <!--
    Этот проект создан YingyanChen. Коммерческое использование запрещено.
    该项目由YingyanChen生成，禁止商用。
    This project was created by YingyanChen. Commercial use is prohibited.
  -->

  # ReadPaper 学术论文阅读辅助系统

  学术论文批量阅读辅助工具。将 PDF 通过 MinerU 转为 Markdown，再由 Claude 深度分析，自动生成结构化 DOCX 阅读笔记，并管理文件状态流转。

  ## 工作流

  \```
  pdf_unread\ ──[/驱动MinerU或/在线MinerU]──→ pdf_done\（PDF 归档）
                                              → md_unread\
  md_unread\  ──[/阅读并总结文献]──────────→ md_done\（MD 归档）
                                              → docx_done\（DOCX 阅读笔记）
  \```

  ## 功能特性

  - **PDF → Markdown 转换**：支持本地 MinerU CLI 或在线 [mineru.net](https://mineru.net) 两种方式
  - **AI 深度分析**：自动提取研究问题、实验方法、结果与讨论，生成结构化摘要
  - **DOCX 阅读笔记生成**：包含双语 Abstract、Introduction 逐段摘要、Methods/Results/Discussion 结构化分析
  - **批量处理**：一次处理 `md_unread/` 下所有 MD 文件，逐篇输出进度
  - **文件状态管理**：处理完成后自动将源文件归档，保持工作目录整洁

  ## 前置依赖

  | 依赖 | 说明 |
  |------|------|
  | [Claude Code](https://claude.ai/code) | 运行 Skill 所需的 AI 编程助手 |
  | Python 3.8+ | 需加入系统 PATH |
  | python-docx | `pip install -r requirements.txt` |
  | MinerU（可选） | 本地转换时需要：`pip install magic-pdf[full]` |
  | mineru.net 账号（可选） | 在线转换时需要，免费注册 |

  ## 安装

  ```bash
  git clone https://github.com/<your-username>/ReadPaper.git
  cd ReadPaper
  pip install -r requirements.txt
  ```

  完成后，在 Claude Code 中打开 `ReadPaper/` 目录，即可使用所有 `/` 命令。

  ## 项目结构

  ```
  ReadPaper/
  ├── .claude/
  │   └── skills/                   # 4 个 Claude Code Skill
  │       ├── 阅读并总结文献/
  │       ├── 批量阅读并总结文献/
  │       ├── 驱动MinerU执行PDF→MD转换/
  │       └── 在线MinerU执行PDF→MD转换/
  ├── scripts/
  │   ├── generate_reading_notes.py  # DOCX 生成脚本
  │   └── cors_server.py             # 在线上传用本地文件服务器
  ├── pdf_unread/                    # 放入待转换的 PDF
  ├── pdf_done/                      # PDF 转换后自动归档至此
  ├── md_unread/                     # MinerU 生成的 MD，待分析
  ├── md_done/                       # 分析完成后 MD 归档至此
  ├── docx_done/                     # 生成的 DOCX 阅读笔记
  ├── requirements.txt
  ├── CLAUDE.md
  └── README.md
  ```

  ## 使用方法

  在 Claude Code 中，于项目目录下输入以下命令：

  ### `/驱动MinerU执行PDF→MD转换`（本地转换）

  将 `pdf_unread/` 中的 PDF 通过本地 MinerU CLI 转为 MD，输出至 `md_unread/`。

  ```
  /驱动MinerU执行PDF→MD转换 [文件名] [--from pdf_unread] [--to md_unread]
  ```

  **前提**：已安装 MinerU：`pip install magic-pdf[full]`

  ### `/在线MinerU执行PDF→MD转换`（在线转换）

  通过 [mineru.net](https://mineru.net) 在线转换 PDF，自动上传、等待解析、下载 MD。网络不可用时自动回退至本地版。

  ```
  /在线MinerU执行PDF→MD转换 [文件名] [--from pdf_unread] [--to md_unread]
  ```

  **前提**：浏览器已登录 mineru.net；使用 Claude in Chrome MCP 插件。

  ### `/阅读并总结文献`（单篇分析）

  读取 `md_unread/` 中的一篇 MD，AI 深度分析后生成 DOCX 阅读笔记，归档 MD。

  ```
  /阅读并总结文献 [文件名] [--from md_unread] [--md-to md_done] [--docx-to docx_done]
  ```

  ### `/批量阅读并总结文献`（批量分析）

  对 `md_unread/` 中所有 MD 文件逐篇执行单篇分析，输出进度与汇总报告。

  ```
  /批量阅读并总结文献 [--from md_unread] [--md-to md_done] [--docx-to docx_done]
  ```

  > **建议**：批量运行前先用单篇验证一遍，确认输出格式正确后再批量。

  ## Skill 说明

  4 个 Skill 已包含在项目的 `.claude/skills/` 目录中，克隆项目后在 Claude Code 里打开目录即可直接使用，无需额外安装。

  若需单独安装这些 Skill（不含项目其余文件），请参见配套插件仓库：
  👉 **[readpaper-skills](https://github.com/<your-username>/readpaper-skills)**

  ## 在线 MinerU 上传说明

  在线版使用本地 CORS 服务器 + 浏览器 DataTransfer API 注入完成文件上传，无需手动操作文件对话框：

  1. Skill 自动启动 `scripts/cors_server.py`（监听 `127.0.0.1:18765`）
  2. 页面弹出的系统文件对话框**无实际作用**，按 `Escape` 关闭即可
  3. 文件通过 JavaScript 直接注入 `<input type="file">` 元素完成上传

  ## MD 文件命名规律

  MinerU 生成的 MD 文件名格式：`MinerU_markdown_[论文标题]_[数字ID].md`

  生成的 DOCX 文件名格式：`[论文标题].docx`（去掉前缀和数字后缀）

  ## License

  本项目仅供学习与个人研究使用，禁止商业用途。
  ```

- [ ] **Step 2: 验证文件结构**

  确认：顶部有版权注释、包含工作流图、4 个命令各有说明、Skill 安装说明已写。

- [ ] **Step 3: Commit**

  ```powershell
  git add README.md
  git commit -m "docs: add README.md with watermark, usage guide, and skill instructions"
  ```

---

## Task 9: 创建 readpaper-skills 插件 Repo

**Files:**
- Create: `../readpaper-skills/.claude/skills/` 下 4 个 SKILL.md（内容同主项目 `.claude/skills/` 中泛化后的版本）
- Create: `../readpaper-skills/README.md`

- [ ] **Step 1: 创建目录结构**

  ```powershell
  $skillsRoot = "..\readpaper-skills\.claude\skills"
  New-Item -ItemType Directory -Force "$skillsRoot\阅读并总结文献"
  New-Item -ItemType Directory -Force "$skillsRoot\批量阅读并总结文献"
  New-Item -ItemType Directory -Force "$skillsRoot\驱动MinerU执行PDF→MD转换"
  New-Item -ItemType Directory -Force "$skillsRoot\在线MinerU执行PDF→MD转换"
  ```

- [ ] **Step 2: 复制 4 个 SKILL.md**

  ```powershell
  $src = ".claude\skills"
  $dst = "..\readpaper-skills\.claude\skills"
  Copy-Item "$src\阅读并总结文献\SKILL.md" "$dst\阅读并总结文献\SKILL.md"
  Copy-Item "$src\批量阅读并总结文献\SKILL.md" "$dst\批量阅读并总结文献\SKILL.md"
  Copy-Item "$src\驱动MinerU执行PDF→MD转换\SKILL.md" "$dst\驱动MinerU执行PDF→MD转换\SKILL.md"
  Copy-Item "$src\在线MinerU执行PDF→MD转换\SKILL.md" "$dst\在线MinerU执行PDF→MD转换\SKILL.md"
  ```

- [ ] **Step 3: 写入 readpaper-skills/README.md**

  内容如下：

  ```markdown
  <!--
    Этот проект создан YingyanChen. Коммерческое использование запрещено.
    该项目由YingyanChen生成，禁止商用。
    This project was created by YingyanChen. Commercial use is prohibited.
  -->

  # readpaper-skills

  [ReadPaper](https://github.com/<your-username>/ReadPaper) 项目的配套 Claude Code Skill 插件包。
  包含 4 个可独立使用的 Skill，用于学术论文的 PDF 转换与 AI 深度阅读分析。

  ## 包含 Skill

  | 命令 | 功能 |
  |------|------|
  | `/驱动MinerU执行PDF→MD转换` | 本地 MinerU CLI 将 PDF 转为 Markdown |
  | `/在线MinerU执行PDF→MD转换` | 通过 mineru.net 在线转换 PDF，自动上传与下载 |
  | `/阅读并总结文献` | AI 深度分析单篇 MD，生成结构化 DOCX 阅读笔记 |
  | `/批量阅读并总结文献` | 批量处理目录下所有 MD 文件 |

  ## 安装

  ### 方法一：Windows PowerShell

  ```powershell
  git clone https://github.com/<your-username>/readpaper-skills.git
  # 将 skills 复制到你的项目
  xcopy readpaper-skills\.claude\skills\ <your-project>\.claude\skills\ /E /I /Y
  ```

  ### 方法二：macOS / Linux

  ```bash
  git clone https://github.com/<your-username>/readpaper-skills.git
  cp -r readpaper-skills/.claude/skills/ <your-project>/.claude/skills/
  ```

  安装后，在 Claude Code 中打开你的项目目录，即可使用以上 `/` 命令。

  ## 依赖

  | 依赖 | 说明 |
  |------|------|
  | [Claude Code](https://claude.ai/code) | 必须 |
  | Python 3.8+（加入 PATH） | `/阅读并总结文献` 和 `/在线MinerU` 需要 |
  | python-docx | `pip install python-docx` |
  | MinerU CLI（可选） | 本地转换：`pip install magic-pdf[full]` |
  | mineru.net 账号（可选） | 在线转换时需要 |
  | Claude in Chrome MCP（可选） | `/在线MinerU执行PDF→MD转换` 需要浏览器控制 |

  ## 项目目录要求

  Skill 运行时会自动以 `CLAUDE.md` 所在目录（或当前工作目录）作为项目根目录，
  并自动探测系统 `python`。你的项目需包含以下目录：

  ```
  your-project/
  ├── pdf_unread/    # 放入待转换的 PDF
  ├── pdf_done/      # PDF 归档（自动创建或手动创建）
  ├── md_unread/     # MinerU 输出的 MD
  ├── md_done/       # 分析后 MD 归档
  ├── docx_done/     # DOCX 阅读笔记输出
  └── scripts/
      ├── generate_reading_notes.py   # 来自主项目
      └── cors_server.py              # 来自主项目（在线版需要）
  ```

  推荐直接使用 [ReadPaper](https://github.com/<your-username>/ReadPaper) 主项目，已包含所有脚本和目录结构。

  ## License

  本项目仅供学习与个人研究使用，禁止商业用途。
  ```

- [ ] **Step 4: 在 readpaper-skills 目录初始化 git 并提交**

  ```powershell
  cd ..\readpaper-skills
  git init
  git add .
  git commit -m "init: readpaper-skills plugin with 4 generalized skill files"
  cd ..\ReadPaper
  ```

---

## Task 10: 最终验证与主项目收尾提交

- [ ] **Step 1: 检查 git status，确认无遗漏**

  ```powershell
  git status
  ```

  预期：所有变更已提交，working tree 干净（或只有应被 gitignore 的文件）。

- [ ] **Step 2: 检查 .gitignore 效果**

  ```powershell
  git ls-files --others --excluded | head -20
  ```

  确认数据目录内容（*.pdf、*.md、*.docx）不在追踪范围内，`.gitkeep` 文件已被追踪。

- [ ] **Step 3: 检查两个 README 中版权水印**

  确认 `README.md` 和 `../readpaper-skills/README.md` 顶部均有三语版权注释。

- [ ] **Step 4: 提醒用户替换 README 中的 `<your-username>`**

  在两个 README.md 中，将所有 `<your-username>` 替换为实际 GitHub 用户名后再推送。

---

## 自审检查（实施前）

- [x] **Spec 覆盖**：水印 ✓、README ✓、.gitignore ✓、requirements.txt ✓、4 个 SKILL.md 泛化 ✓、skills repo ✓
- [x] **占位符**：README 中 `<your-username>` 是预留的占位符，Task 10 Step 4 有说明 ✓
- [x] **一致性**：各 SKILL.md 泛化策略统一（相对路径 + 系统 python + PowerShell 动态 root）✓
- [x] **歧义**：`.gitkeep` 目录策略在 .gitignore 和 Task 3 中一致（`*.pdf` 不是 `pdf_done/`）✓
