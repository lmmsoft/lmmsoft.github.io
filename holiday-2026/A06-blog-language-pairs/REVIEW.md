---
title: "A06 博客多语言发布：接入提案与审阅决策"
type: review
source: repository-review-and-proposed-contract
created: 2026-10-04
status: needs-review
tags:
  - hreflang
  - canonical
  - rss
---

# A06 博客多语言发布

## 已作出的演示决策

- 内容 locale 使用 BCP 47 风格的 `zh-CN`、`en`、`zh-TW`，不复用主题 UI 的 `cn` 键。
- `translation_group_id` 一经分配不可因标题或 slug 修改而改变。
- 源文件完整字节参与 SHA-256；任何 frontmatter 或正文变化都会让译稿 stale。
- `reviewed` 仅表示人工完成当前 revision 的语义审阅；工具不能自行赋予它。
- 构建预览不是授权发布。有效状态不是 `reviewed` 的译稿必须从生产构建集合中排除，而不是只显示警告。

## 拟议生产兼容契约（尚未接入）

### URL

保留现有中文 URL 作为不可破坏的稳定地址。新译文建议位于 `/i18n/<locale>/<existing-slug>/`；`translation_group_id` 只作为数据键，不暴露为必须稳定的 URL。不得批量改写旧中文 permalink。冲突与非 ASCII slug 要在接入前列清单人工裁决。

### canonical

每个语言页面 canonical 指向自己最终的绝对 URL，不把英语/繁体 canonical 回中文，否则搜索引擎可能把译文视为重复页。预览页输出 `noindex`（真正接入时新增）；当前任务目录不会进入生产布局。

### hreflang

仅为存在且 `reviewed`、非 stale 的版本输出 `<link rel="alternate" hreflang="…">`。每个集合成员都输出相同的互返集合；中文源为 `zh-CN`，繁体为 `zh-TW`，英语为 `en`。`x-default` 指现有中文 URL。缺译稿时不伪造链接。

### RSS/Atom

保留当前 `/feed.atom` 和 `/feed.xml` 行为以兼容订阅者。新增语言 feed 时使用 `/i18n/<locale>/feed.atom`，只收录该 locale 且可发布的内容；entry id 永久取规范 URL。是否把译文混入主 feed 必须由维护者另行决定，默认不混入以避免突然三倍推送。

## 真正接入所需修改

1. 在 `_data/` 引入经过审核的配对索引或 Jekyll collection，并定义构建前校验命令。
2. 为文章 frontmatter 增加 `translation_group_id`、`locale`、`source_revision`、译文的 `source_hash`/`review_status`。
3. 修改 `_includes/head.html` 输出自指 canonical、互返 hreflang 与 x-default；先建立 URL 快照回归测试。
4. 修改/新增布局语言切换器，只枚举可发布成员；stale 和 unreviewed 不得出现在生产集合。
5. 明确 `jekyll-feed` 的过滤能力；若不足，新增受测试的语言 feed 模板。
6. 在 Docker 内运行生产构建与 `jekyll doctor`，再检查旧 URL、分页、首页、站点地图、桌面/手机布局。

以上均为提案。本任务没有改 `_config.yml`、`_includes/`、`_layouts/`、生产正文或路由。

## 待人工 review

- 是否接受 URL 前缀 `/i18n/` 及 locale 拼写。
- 英文是否用 `en` 还是区域码；`x-default` 是否永远指中文。
- 主 feed 是否只保留源稿、语言 feed 的发现方式。
- 谁可以设置 `reviewed`，是否需要 reviewer 与 reviewed_at 字段。
- 段落级语义对齐是否需要独立工具，而非当前结构性门禁。
