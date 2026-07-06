# 在线MinerU执行PDF→MD转换

当用户输入 `/在线MinerU执行PDF→MD转换` 时，严格按以下步骤执行。

## 项目根目录

Claude Code 启动时已自动切换至项目根目录（即包含 `CLAUDE.md` 的目录）。
后续所有相对路径均以此为基础。

## 参数解析

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `文件名` | 目标 PDF 文件名（可带或不带 `.pdf`） | 来源文件夹中**所有** PDF 文件 |
| `--from 路径` | PDF 来源文件夹（绝对路径或相对于项目根目录） | `pdf_unread` |
| `--to 路径` | MD 输出文件夹（绝对路径或相对于项目根目录） | `md_unread` |

PDF 归档目标（固定，不可修改）：项目根目录下的 `pdf_done`

---

## 执行步骤

### 第 1 步：确定完整路径

- 来源文件夹 A = `--from` 值 或 当前目录下的 `pdf_unread`
- 输出文件夹 B = `--to` 值 或 当前目录下的 `md_unread`
- PDF 归档目标 = 当前目录下的 `pdf_done`

### 第 2 步：找到目标 PDF

使用 Glob 工具列出文件夹 A 中所有 `.pdf` 文件：

- 若用户指定了文件名：找到匹配文件（自动补全 `.pdf` 后缀），仅处理该一个文件
- 若未指定：取文件夹 A 中**所有** `.pdf` 文件（字母顺序排列）
- 若文件夹 A 中没有 PDF：告知用户"【文件夹A】中没有找到 PDF 文件"，停止执行

列出待处理 PDF 清单，告知用户共找到 N 个文件。

### 第 3 步：检查网络连通性

```powershell
Test-Connection mineru.net -Count 1 -Quiet
```

**若返回 `True`**：网络正常，继续执行。

**若返回 `False`**：询问用户：
> "网络不可用，无法访问 mineru.net。是否改用本地 MinerU 进行转换？"

- 若用户选择**使用本地版**：
  1. 检查本地 MinerU 是否已安装：
     ```powershell
     (Get-Command mineru -ErrorAction SilentlyContinue) -ne $null
     ```
  2. 若**已安装**：切换执行 `/驱动MinerU执行PDF→MD转换` Skill 的逻辑，停止本 Skill
  3. 若**未安装**：询问用户：
     > "本地 MinerU 未安装。是否立即安装？安装命令为：`pip install mineru[all]`"
     - 若用户确认安装：执行安装，安装完成后切换至本地版 Skill 逻辑
     - 若用户不安装：告知"无法继续转换"，停止执行

- 若用户选择**不使用本地版**：停止执行

### 第 4 步：打开浏览器并导航到 MinerU

1. 使用 `mcp__Claude_in_Chrome__tabs_context_mcp`（createIfEmpty: true）获取标签页
2. 若提示选择浏览器，询问用户选择哪个
3. 导航到：`https://mineru.net/OpenSourceTools/Extractor`
4. 等待页面加载（wait 2秒），截图确认

### 第 5 步：检查登录状态

截图检查页面：

- **已登录**：左侧边栏出现蓝色"新解析"按钮 → 继续执行
- **未登录**：告知用户：
  > "尚未登录 MinerU，请在浏览器中登录账号后告知我"

  等待用户回复后截图确认已登录，然后继续。

### 第 6 步：上传 PDF 文件

**首次上传前**，启动 CORS 文件服务器（用于浏览器读取本地 PDF）：

```powershell
$root = (Get-Location).Path
$pdfFolder = "$root\pdf_unread"
$pyExe = (Get-Command python -ErrorAction Stop).Source
$corsScript = "$root\scripts\cors_server.py"
$procId = (Start-Process -FilePath $pyExe -ArgumentList "$corsScript","$pdfFolder" -WindowStyle Hidden -PassThru).Id
Start-Sleep -Seconds 1
Write-Output "CORS server started (PID: $procId)"
```

对**每一个**待处理 PDF，依次执行以下操作：

1. 确认当前在上传页面（截图检查是否有"上传文件"按钮）
   - 若不在上传页面：点击左侧边栏"新解析"按钮返回上传页面
2. **直接**通过浏览器 JavaScript 使用 DataTransfer API 将文件注入页面的 `<input type="file">` 元素（**无需点击"上传文件"按钮**，该按钮只是视觉入口，`input` 元素在页面加载时已存在于 DOM）：
   ```javascript
   (async () => {
     const fileName = "【当前PDF文件名（仅文件名，不含路径）】";
     const encodedName = encodeURIComponent(fileName);
     const resp = await fetch(`http://127.0.0.1:18765/${encodedName}`);
     const blob = await resp.blob();
     const file = new File([blob], fileName, {type: 'application/pdf'});
     const dt = new DataTransfer();
     dt.items.add(file);
     const input = document.querySelector('input[type="file"]');
     if (!input) throw new Error('input[type="file"] not found');
     input.files = dt.files;
     input.dispatchEvent(new Event('change', {bubbles: true}));
     return 'File injected: ' + fileName + ' (' + blob.size + ' bytes)';
   })()
   ```
   - 若 JS 报错 `input[type="file"] not found`：说明当前页面 input 尚未渲染，此时先点击"📎 上传文件"按钮（会弹出 OS 文件对话框），然后**不关闭对话框**，直接再次执行上述 JS 注入，注入成功后对话框会自动消失或留在后台（不影响上传）
3. 截图确认文件已被选中并开始上传

**所有 PDF 上传完毕后**：
- 记录本次上传的文件名列表（用于第 8 步过滤）
- 关闭 CORS 服务器：
  ```powershell
  Stop-Process -Id $procId -Force -ErrorAction SilentlyContinue
  ```

### 第 7 步：等待所有文件解析完成

上传后，MinerU 开始在线处理。每隔 30 秒截图一次，观察左侧边栏文件列表：

- 所有本次上传的文件旁均出现"✅ 解析成功"标记 → 继续
- 部分文件仍在处理中 → 继续等待

**超时处理**：若等待超过 15 分钟仍有文件未完成，告知用户：
> "在线解析已超过 15 分钟，以下文件仍未完成：【文件名列表】。是否继续等待？"

等待用户指示后决定是否继续。

### 第 8 步：依次进入结果页并下载

**仅处理本次上传的 PDF 对应的结果**，不操作历史任务。

对**每一个**本次上传的 PDF，依次执行：

1. 在左侧边栏中找到该文件名并点击，进入结果页
2. 等待结果页加载（wait 2秒），截图确认
3. 确认页面 URL 格式为：`https://mineru.net/OpenSourceTools/Extractor/PDF/{task_id}`
4. 确认右侧"Markdown"标签页有内容显示
5. 执行**第 9 步**（下载并检查文件名）
6. 执行**第 10 步**（移动文件、归档 PDF）
7. 返回上传页面（点击左上角 `<` 返回或点击"新解析"），处理下一个文件

### 第 9 步：下载 Markdown 并检查文件名

1. 在结果页右上角找到两个相邻图标按钮：左侧是分享/导出按钮（"导出到 Notion / 导出到 Dify"），右侧是**下载按钮（↓）**
2. 点击**右侧下载按钮（↓）**，弹出下拉菜单
3. 在菜单中点击最下方的"**下载Markdown**"选项
4. 等待 3 秒，文件自动下载到浏览器默认下载文件夹

**检查文件名格式**：

使用 PowerShell 找到刚下载的最新 `.md` 文件：

```powershell
$downloads = "$env:USERPROFILE\Downloads"
$latest = Get-ChildItem "$downloads\*.md" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
$latest.Name
```

- 若文件名**符合** `MinerU_markdown_*` 格式 → 直接进入第 10 步
- 若文件名**不符合**：将其重命名为规范格式：

```powershell
$pdfTitle = [System.IO.Path]::GetFileNameWithoutExtension("【当前PDF文件名】")
$newName = "MinerU_markdown_$pdfTitle.md"
Rename-Item $latest.FullName "$downloads\$newName"
Write-Output "已重命名：$($latest.Name) → $newName"
```

### 第 10 步：移动 MD 文件并归档 PDF

**移动 MD 文件**到输出文件夹 B：

```powershell
$downloads = "$env:USERPROFILE\Downloads"
$mdFile = Get-ChildItem "$downloads\MinerU_markdown_*.md" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if ($mdFile) {
    Move-Item $mdFile.FullName "【文件夹B】\$($mdFile.Name)" -Force
    Write-Output "已移动：$($mdFile.Name)"
} else {
    Write-Output "⚠️ 未找到 MD 文件，请检查浏览器下载目录"
}
```

**归档原始 PDF** 到 `pdf_done`：

```powershell
$root = (Get-Location).Path
Move-Item "【当前PDF完整路径】" "$root\pdf_done\【当前PDF文件名】" -Force
```

### 第 11 步：报告结果

所有文件处理完毕后，输出汇总报告：

```
已完成在线 MinerU 转换，共处理 N 个文件：

✓ 【PDF文件名1】
  MD 文件：【MD文件路径1】
  PDF 已归档至：pdf_done\【PDF文件名1】

✓ 【PDF文件名2】
  MD 文件：【MD文件路径2】
  PDF 已归档至：pdf_done\【PDF文件名2】

（如有失败项，在此列出并说明原因）
```

---

## 注意事项

- **登录状态**：浏览器 Cookie 会保持登录状态，通常无需每次重新登录
- **服务限制**：单文件 ≤200 页，单日上限 5000 份；超出时 MinerU 会提示错误，告知用户后停止
- **文件命名**：下载 MD 文件名格式为 `MinerU_markdown_{标题}_{ID}.md`，与本地工具命名规律一致
- **历史任务过滤**：第 8 步只处理本次 Session 上传的文件，通过对比第 6 步记录的文件名列表来区分
