<!--
  Этот проект создан YingyanChen. Коммерческое использование запрещено.
  该项目由YingyanChen生成，禁止商用。
  This project was created by YingyanChen. Commercial use is prohibited.
-->

# ReadPaper 学术论文阅读辅助系统

学术论文批量阅读辅助工具。将 PDF 通过 MinerU 转为 Markdown，再由 Claude 深度分析，自动生成结构化 DOCX 阅读笔记，并管理文件状态流转。

## 工作流

```
pdf_unread\ ──[/驱动MinerU或/在线MinerU]──→ pdf_done\（PDF 归档）
                                            → md_unread\
md_unread\  ──[/阅读并总结文献]──────────→ md_done\（MD 归档）
                                            → docx_done\（DOCX 阅读笔记）
```

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
git clone https://github.com/CrisChenYingyan/ReadPaper.git
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

👉 **[readpaper-skills](https://github.com/CrisChenYingyan/readpaper-skills)**

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
