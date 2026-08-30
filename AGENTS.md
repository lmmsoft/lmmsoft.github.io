# 全局协作指南（统一版）

本指南面向所有模型（Claude、Qwen、Gemini 等），统一使用本文件作为上下文来源。

## 项目概述
- 这是一个基于 Jekyll 的个人博客（19 年内容，437 篇文章，2006-2025），托管在 GitHub Pages。
- 主题采用 Freshman21，自定义导航与多语言界面（默认中文，兼容英语、日语、波兰语、韩语、俄语、土耳其语、印尼语）。
- 内容涵盖 ACM 竞赛、旅行、技术成长、个人随笔等，资产放在 `images/`、`attachments/`。

## 开发与运行
- 这是个 ruby jekyll 项目， 希望在 docker 容器里运行相关的安装构建命令。
- 本地预览：`./_preview.sh`（含草稿和未来文章，端口 4000）。
- Docker 预览：`make serve`（Jekyll 3.8.5，端口 3000/4000）。
- 生产构建：`make build` 或 `bundle exec jekyll build`。
- 健康检查：`jekyll doctor`。

## 内容管理工作流
1. 创建草稿：`./_new_draft.sh 文章标题`（生成 `_drafts/` 模板）。
2. 编辑草稿并在 `_drafts/` 中预览（`_preview.sh`/`make serve`）。
3. 发布：`./_publish.sh _drafts/<文件名>.md`（自动加日期前缀并移动到 `_posts/`）。
4. 发布前运行排版工具：`pangu -f` 与 `tekorrect -f`。

## 旅行页工作流

- 旅行页模板为 `f_travel.md`，公开数据的单一事实源是 `_data/travel.yml`。
- 数据必填字段为 `id`、`date`、`place`、`spots`，`title` 是可选的行程主题：只存纯文本，模板会渲染为 `【标题】`，不要把方括号写入 YAML；当 `title` 与 `place` 相同时，页面只显示标题，避免重复。年份由上层分组提供；单日使用 `月-日`，连续行程使用 `月-日~月-日`；中国行程只写城市，境外行程写“国家-城市”。
- 创建或发布游记时，在文章 frontmatter 增加对应的 `travel_id`。旅行页会按 `travel_id` 自动发现已发布文章并生成站内相对链接。
- 有已发布游记且能确认实际出行日期时，必须在 `_data/travel.yml` 建立或补全对应行程。没有文章的已完成行程，只要日期、城市和旅行性质能够确认，也可以展示。
- 相邻日期属于同一次出行时，聚合为一条行程：合并日期范围、城市、景点和所有相关文章，不要逐日拆分。
- 候选信息可来自 `f_list.md`、已发布文章和人工审核后的外部私人记录；仓库文档不得出现私人记录的本地路径，构建过程不得直接读取私人知识库。
- 默认只公开已发生的行程。未来计划、住宿、家庭住址、交通班次和其他可推断实时位置的信息不得自动写入旅行页。
- 修改旅行页或游记关联后，不要求本地运行 Docker/Jekyll 生产构建。推送 GitHub PR 后，必须等待 Vercel CI 成功，并在 Vercel 预览站点检查 `/travel/` 的桌面和手机布局、导航顺序及文章链接。

## 结构与命名
- 文章文件名：`YYYY-MM-DD-标题-使用-连字符.md`，日期不可为未来。
- Slug 需用英文并尽量与 permalink 一致（例：`/migration_to_obsidian_for_ai/` 对应 `YYYY-MM-DD-migration_to_obsidian_for_ai.md`）。
- YAML Front Matter：两空格缩进，至少包含 `layout`、`title`、`date`、`categories`/`tags`。
- 布局与组件：修改放在 `_layouts/`、`_includes/`、`_sass/`，主样式在 `css/main.scss`。
- 导航顺序在 `_includes/header.html` 中显式维护；旅行页 `f_travel.md` 必须位于 `f_list.md`（“我的清单”）之后。
- 媒体与附件：放入 `images/` 或 `attachments/`，按日期或主题组织。

## 内容规范
- 首页摘要使用单个 `<!--more-->` 标记（发布前务必检查）。
- 大改版本可在文章末尾添加 changelog，注明时间与改动内容。
- Markdown 使用语义化标题与围栏代码块；Sass 采用四空格缩进与单引号。
- 中文内容发布前运行 `pangu`/`tekorrect` 以优化排版。

## 测试与质量门禁
- 普通文章、媒体和旅行数据变更不要求本地运行 Docker/Jekyll 构建；本地构建只作为按需排障手段。
- 推送 GitHub PR 后，必须等待 Vercel CI 任务成功，并在 Vercel 预览站点检查相关页面的内容、图片、链接以及桌面和手机布局。
- 升级依赖、修改 `_config.yml` 或构建流程时，按需运行本地生产构建和 `jekyll doctor`，同时仍须通过 Vercel CI 与预览验证。

## 提交与评审
- 提交信息遵循 `ADD: …`、`FIX: …`、`CHORE: …` 前缀，保持单一关注点。
- PR 需概述意图、记录 Vercel CI 与预览验证结果，必要时附截图（UI 变更）；如额外运行了本地检查，再列出相应命令。

## 工具与集成
- 分析：Google Analytics 4、Plausible.io、不蒜子；评论：Disqus；订阅：jekyll-feed。
- Gemini CLI 通过 `.gemini/settings.json` 指定本文件为上下文（已在仓库内配置）：
  ```json
  { "contextFileName": "AGENTS.md" }
  ```
- Qwen Code CLI 同样支持 `contextFileName`，已在 `.qwen/settings.json` 映射到本文件。

## 兼容性说明
- 本文件取代原有的 QWEN.md 与 GEMINI.md 配置说明，请统一查阅此处；保留 CLAUDE.md 作为补充背景。
