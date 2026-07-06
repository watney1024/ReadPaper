# 驱动MinerU执行PDF→MD转换

当用户输入 `/驱动MinerU执行PDF→MD转换` 时，严格按以下步骤执行。

## 项目根目录

Claude Code 启动时已自动切换至项目根目录（即包含 `CLAUDE.md` 的目录）。
后续所有相对路径均以此为基础。

## 参数解析

从用户消息中提取以下参数（均为可选）：

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `文件名` | 目标 PDF 文件名（可带或不带 `.pdf`） | 来源文件夹中字母顺序第一篇 |
| `--from 路径` | PDF 来源文件夹（绝对路径或相对于项目根目录） | `pdf_unread` |
| `--to 路径` | MD 输出文件夹（绝对路径或相对于项目根目录） | `md_unread` |
| `--language` | OCR 语言代码（`en`/`ch`/`japan` 等） | `en` |
| `--all` | 批量转换文件夹 A 中所有 PDF（见下方"批量模式"） | 未指定则单篇 |

PDF 归档目标（固定，不可修改）：项目根目录下的 `pdf_done`

## 批量模式

当需要一次转换多篇 PDF 时（如用户说"全部转换"、`--all`，或指定多个文件名），按批量模式执行：

- **第 2 步**：列出文件夹 A 中所有 `.pdf` 文件（或用户指定的多篇），按字母顺序排列
- **第 3 步**：调用 `mineru_parse_documents` 时，将所有 PDF 完整路径一次性传入 `file_sources` 数组（如 `["路径1", "路径2", ...]`），MinerU 支持批量解析，比逐篇调用更高效
- **第 4–8 步**：对返回结果 `results` 数组中的每一篇，依次执行获取内容、提取标题、保存 MD、归档 PDF
- **第 9 步**：逐篇报告结果，最后汇总成功/失败数量

批量模式下仍使用单一的 `output_dir`（`文件夹B/_mineru_temp`），所有结果文件在该目录下以原 PDF 文件名（去 `.pdf` 加 `.md`）命名。

## 前置条件

本 Skill 依赖 `mineru_parse_documents` MCP 工具（由 `.opencode/opencode.jsonc` 中配置的 `mineru` MCP 服务器提供）。
若该工具不可用，告知用户"MinerU MCP 未连接，请检查 .opencode/opencode.jsonc 配置并重启 opencode"，停止执行。

## 执行步骤

### 第 1 步：确定完整路径

- 来源文件夹 A = `--from` 值 或 当前目录下的 `pdf_unread`
- 输出文件夹 B = `--to` 值 或 当前目录下的 `md_unread`
- PDF 归档目标 = 当前目录下的 `pdf_done`

### 第 2 步：找到目标 PDF

使用 Glob 工具列出文件夹 A 中所有 `.pdf` 文件：

- 若用户指定了文件名：找到匹配文件（自动补全 `.pdf` 后缀）
- 若指定 `--all` 或多个文件名：取全部 PDF（进入批量模式，见上方"批量模式"）
- 若未指定：取字母顺序第一个 `.pdf` 文件
- 若文件夹 A 中没有 PDF：告知用户 "【文件夹A】中没有找到 PDF 文件"，停止执行

### 第 3 步：调用 MinerU MCP 工具执行转换

调用 `mineru_parse_documents` MCP 工具，参数如下：

- `file_sources`：`["【PDF完整路径】"]`
- `language`：`--language` 值或 `"en"`
- `output_dir`：`"【文件夹B】/_mineru_temp"`

等待工具返回结果。返回值为 JSON，结构如下：

```json
{
  "status": "success",
  "results": [
    {
      "filename": "原PDF文件名",
      "status": "success",
      "content": "Markdown内容（可能被截断）",
      "truncated": true/false,
      "extract_path": "完整MD保存路径（仅截断时存在）",
      "content_chars": 55000
    }
  ],
  "summary": { "total_files": 1, "success_count": 1, "error_count": 0 },
  "message": "Parsing complete! ..."
}
```

若 `results[0].status` 为 `"error"`：告知用户错误信息 `results[0].error`，停止执行。

### 第 4 步：获取完整 Markdown 内容

根据返回结果获取完整 Markdown：

- 若 `truncated` 为 `true` 且 `extract_path` 存在：使用 Read 工具读取 `extract_path` 指向的文件
- 若 `truncated` 为 `false`：直接使用 `content` 字段的内容
- 若 `content` 字段不存在且 `extract_path` 存在：使用 Read 工具读取 `extract_path`

### 第 5 步：提取论文标题并生成文件名

从 Markdown 内容的第一个 `# ` 标题行提取论文标题（去掉前缀 `# ` 和首尾空格）。

若提取到的标题为全大写（如 `DISCOVERING LOW-PRECISION NETWORKS ...`），转换为 Title Case（每个词首字母大写、其余小写，连字符后的词首字母也大写），以提升可读性。示例：`DISCOVERING LOW-PRECISION NETWORKS` → `Discovering Low-Precision Networks`。同时修复因 PDF 换行导致的单词断开（如 `EMBED-DED` → `Embedded`）。

生成 MD 文件名：
1. 将标题中的空格替换为下划线 `_`
2. 生成数字 ID：使用当前时间戳（如 `date +%s` 的输出）
3. 组合文件名：`MinerU_markdown_{标题中下划线连接}_{数字ID}.md`

示例：
- 标题：`Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference`
- 文件名：`MinerU_markdown_Quantization_and_Training_of_Neural_Networks_for_Efficient_Integer-Arithmetic-Only_Inference_1783323398.md`

若 Markdown 第一个 `# ` 标题无法提取（如内容不以 `# ` 开头），则从 PDF 文件名提取标题：
取 PDF 文件名中最后一个 ` - ` 之后、`.pdf` 之前的部分作为标题。

### 第 6 步：保存 MD 文件到文件夹 B

使用 Write 工具将完整 Markdown 内容保存至：
`【文件夹B】/【第5步生成的文件名】`

### 第 7 步：清理临时目录

使用 Bash 工具删除临时目录：

```bash
rm -rf "【文件夹B】/_mineru_temp"
```

### 第 8 步：归档原始 PDF

将 PDF 文件从文件夹 A 移动到 PDF 归档目标（`pdf_done`）。

### 第 9 步：报告结果

向用户输出：

```
✓ 已转换：【PDF文件名】
✓ MD 文件保存至：【文件夹B】/【MD文件名】
✓ 原始 PDF 已归档至：pdf_done/【PDF文件名】
```
