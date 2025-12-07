# `generate_content_index.py` 设计说明

## 目标
- 在仓库根目录生成 `CONTENT_INDEX.md`，汇总 `_posts/` 与 `_drafts/`（兼容 `_post/`、`_draft/`）中的文章。
- 按年份分组、日期降序输出表格，列为：日期 | 标题 | 是否发布 | 类型(post/draft) | 有图片 | 相对路径 | 备注。
- 标记图片来源：本地(`images/`/`attachments/`)、外链、混合或其他；缺失日期文件默认使用 1970-01-01 并打印警告。

## 输入/输出（固定，不提供 CLI 参数）
- 输入目录：`_posts/`, `_drafts/`（兼容 `_post/`, `_draft/`）
- 输出文件：`CONTENT_INDEX.md`（仓库根目录）
- 运行方式：`python scripts/generate_content_index.py`

## 核心流程
1) **扫描文件**：遍历输入目录中所有 `.md` 文件。
2) **解析 Front Matter**：提取 `date`、`title`、`published`，正文用于图片检测。
3) **元信息推断**  
   - 日期：优先 front matter 的 `date`，否则用文件名前缀 `YYYY-MM-DD`，都缺失则警告并用 `1970-01-01`。  
   - 标题：优先 front matter 的 `title`，否则用文件名去除日期前缀。  
   - 类型：路径判定 `post` / `draft`。  
   - 发布状态：`published: true` → ✅，否则 ❌。  
   - 图片：匹配 Markdown/HTML `<img>`。包含 `images/` 或 `attachments/` 记为本地；`http(s)://` 为外链；两者兼有为混合；其他路径记为其他。  
     - 有图列显示：本地 → 🖼️，外链 → 🌐，混合 → 🔀，其他 → ❓，无图 → ➖。  
   - 相对路径：输出相对仓库根目录的文件路径，并将标题/路径渲染为 GitHub 可跳转的链接。  
   - 备注：外链/混合图片标记“含外链图片”；未知路径标记“图片路径需确认”；缺失日期标记“日期需补充”。  
4) **排序与分组**：记录按日期降序排列，并按年份降序分组，标题包含该年 发布/待发布/草稿 数量：
   - 发布：目录在 `_posts/` 且 `published: true`
   - 待发布：目录在 `_posts/` 且 `published: false` 或缺失
   - 草稿：目录在 `_drafts/`
5) **渲染 Markdown**：文件头包含生成时间、用途、运行方式；每个年份一个表格（含相对路径与链接、emoji 状态）。
6) **写入输出**：覆盖生成 `CONTENT_INDEX.md`。

## 备注
- 解析日期时尝试多种格式和 `fromisoformat`，以兼容常见 Jekyll 日期写法（含时区）。
- 若 front matter YAML 解析异常，会输出警告并继续处理正文。
- 若未安装 PyYAML，会降级到简易行级解析（只处理 `key: value/true/false`），复杂结构可能丢失字段。
- 文件名中 `|` 会被转义以避免破坏表格。
