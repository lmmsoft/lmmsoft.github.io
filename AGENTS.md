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

## 结构与命名
- 文章文件名：`YYYY-MM-DD-标题-使用-连字符.md`，日期不可为未来。
- Slug 需用英文并尽量与 permalink 一致（例：`/migration_to_obsidian_for_ai/` 对应 `YYYY-MM-DD-migration_to_obsidian_for_ai.md`）。
- YAML Front Matter：两空格缩进，至少包含 `layout`、`title`、`date`、`categories`/`tags`。
- 布局与组件：修改放在 `_layouts/`、`_includes/`、`_sass/`，主样式在 `css/main.scss`。
- 导航页面按前缀排序：`a_home.md`、`b_about.md`、`c_archives.md`、`d_category.md`、`e_tags.md`、`f_guestbook.md`、`f_list.md`。
- 媒体与附件：放入 `images/` 或 `attachments/`，按日期或主题组织。

## 内容规范
- 首页摘要使用单个 `<!--more-->` 标记（发布前务必检查）。
- 大改版本可在文章末尾添加 changelog，注明时间与改动内容。
- Markdown 使用语义化标题与围栏代码块；Sass 采用四空格缩进与单引号。
- 中文内容发布前运行 `pangu`/`tekorrect` 以优化排版。

## 测试与质量门禁
- 将 `bundle exec jekyll build`（或 `make build`）视为发布门槛，需无报错/警告。
- 升级依赖或改动 `_config.yml` 后运行 `jekyll doctor`。

## 提交与评审
- 提交信息遵循 `ADD: …`、`FIX: …`、`CHORE: …` 前缀，保持单一关注点。
- PR 需概述意图、列出执行的命令（如 `jekyll build`）、必要时附截图（UI 变更）。

## 工具与集成
- 分析：Google Analytics 4、Plausible.io、不蒜子；评论：Disqus；订阅：jekyll-feed。
- Gemini CLI 通过 `.gemini/settings.json` 指定本文件为上下文（已在仓库内配置）：
  ```json
  { "contextFileName": "AGENTS.md" }
  ```
- Qwen Code CLI 同样支持 `contextFileName`，已在 `.qwen/settings.json` 映射到本文件。

## 兼容性说明
- 本文件取代原有的 QWEN.md 与 GEMINI.md 配置说明，请统一查阅此处；保留 CLAUDE.md 作为补充背景。
