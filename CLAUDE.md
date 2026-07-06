<!--
  Этот проект создан YingyanChen. Коммерческое использование запрещено.
  该项目由YingyanChen生成，禁止商用。
  This project was created by YingyanChen. Commercial use is prohibited.
-->

# ReadPaper 学术论文阅读辅助系统

## 项目简介
学术论文批量阅读辅助工具。通过 MinerU 将 PDF 转为 Markdown，
再由本项目 AI 深度分析，生成结构化 MD 阅读笔记，并管理文件状态流转。

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
| `md_done\`    | 已生成阅读笔记的 MD 归档 |
| `docx_done\`  | 生成的论文阅读笔记 MD |

## 可用命令

| 命令 | 参数 | 说明 |
|------|------|------|
| `/驱动MinerU执行PDF→MD转换` | `[文件名] [--all] [--from A] [--to B] [--language L]` | PDF→MD 转换（MinerU MCP 云端 API），默认 A=pdf_unread B=md_unread L=en；`--all` 批量转换全部 |
| `/在线MinerU执行PDF→MD转换` | `[文件名] [--from A] [--to B]` | ~~已废弃~~，被 `/驱动MinerU执行PDF→MD转换`（MCP 版）取代 |
| `/阅读并总结文献` | `[文件名] [--from C] [--md-to D] [--docx-to E]` | 单篇分析，默认 C=md_unread D=md_done E=docx_done |
| `/批量阅读并总结文献` | `[--from C] [--md-to D] [--docx-to E]` | 批量分析，参数同上 |

## 技术栈
- MinerU MCP（`mineru-open-mcp`，通过 `.opencode/opencode.jsonc` 配置，需 `MINERU_API_TOKEN`）
- MCP 工具：`mineru_parse_documents`（PDF/图片/Word→Markdown）、`mineru_get_ocr_languages`
- ~~`scripts/cors_server.py`~~（仅废弃的在线 Skill 使用，MCP 版不再需要）

## Skill 包
项目使用的 Skill 集中在 `.claude/skills/` 下，作为一个整体使用：

| Skill | 路径 | 触发命令 | 依赖 |
|-------|------|---------|---------|
| PDF→MD 转换（MCP） | `.claude/skills/驱动MinerU执行PDF→MD转换/SKILL.md` | `/驱动MinerU执行PDF→MD转换` | MinerU MCP |
| PDF→MD 转换（在线·废弃） | `.claude/skills/在线MinerU执行PDF→MD转换/SKILL.md` | `/在线MinerU执行PDF→MD转换` | ~~`scripts/cors_server.py`~~ |
| 单篇精读 | `.claude/skills/阅读并总结文献/SKILL.md` | `/阅读并总结文献` | — |
| 批量精读 | `.claude/skills/批量阅读并总结文献/SKILL.md` | `/批量阅读并总结文献` | — |

四个 Skill 构成完整流水线，需作为一组同步维护（修改某一个时检查其他三个是否需要联动更新）。

## 运行规范

### 批量运行策略
执行 `/批量阅读并总结文献` 前，**必须先用单篇跑通**：
1. 取 `md_unread\` 中第一个 MD 文件，执行 `/阅读并总结文献` 验证
2. 确认 MD 笔记生成正确、MD 归档无误后，再执行批量命令
3. 批量阶段默认逐篇串行处理；仅在用户明确要求且单篇验证通过后，才考虑并行方案

### 最小改动原则
修改任何文件（Skill、脚本、配置）时：
- 只改动与当前需求直接相关的部分
- 不顺手重构、不扩展未被要求的功能
- 改动前说明"改了什么、为什么改"

### 运行后清理（暂停中）
~~每次运行完毕后执行以下清理，确保工作目录干净：~~
~~- 删除临时文件：`scripts/_temp_analysis.json`（正常流程自动清理，异常中断时手动删除）~~
~~- 卸载本次为尝试某方案临时安装但最终未使用的 Python 包~~
~~- 删除下载但未使用的文件（安装包、临时脚本等）~~

### 运行后询问
**每次执行任意命令结束后**，都询问用户：
> "是否需要更新 CLAUDE.md？（例如：新增规范、修正文件路径、记录本次发现的问题）"

## ~~在线 MinerU 操作说明~~（已废弃，被 MCP 取代）

> 以下内容仅作历史参考，当前使用 `/驱动MinerU执行PDF→MD转换`（MCP 版）替代。

### 文件上传方式
使用 CORS 服务器 + 浏览器 DataTransfer API 注入，而非通过 Windows 文件对话框：

1. 上传前启动 `scripts/cors_server.py`（监听 `127.0.0.1:18765`，服务 `pdf_unread` 目录）
2. 点击页面"上传文件"按钮后，**会自动弹出 Windows 文件选择对话框——该对话框对实际上传无任何作用，立即按 `Escape` 关闭**
3. 通过浏览器 JavaScript 从 CORS 服务器 fetch 文件为 Blob，经 DataTransfer API 注入到 `<input type="file">` 元素完成上传
4. 所有文件上传完毕后停止 CORS 服务器进程

### Markdown 下载按钮位置
结果页右上角有两个相邻图标：**左侧**为分享/导出按钮（点击显示"导出到 Notion / 导出到 Dify"），**右侧**为下载按钮（↓）。点击右侧下载按钮，在弹出菜单最下方选择"**下载Markdown**"。

## MD 文件命名规律（MinerU 生成）
`MinerU_markdown_[论文标题]_[数字ID].md`

## 笔记文件命名规则
去掉 `MinerU_markdown_` 前缀和末尾 `_[数字ID]` 后缀，得到论文标题，加 `.md`。
