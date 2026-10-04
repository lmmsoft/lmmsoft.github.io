---
title: "A05 短内容／微博客时间流 — PRD"
type: prd
source: task-input-and-public-repository
created: 2026-10-04
status: needs-review
tags: [A05, microblog, demo]
---

# A05 短内容／微博客时间流

## 目标与范围

在不新增 CMS、不改生产导航、RSS、文章或根配置的前提下，验证短内容的时间倒序、标签筛选、永久锚点、空状态与移动端阅读。演示只使用 8 条明确标为 DEMO 的合成内容；默认隐藏其中 1 条草稿。

## 输入与输出

输入是 `content/*.md`，短内容 frontmatter 必填 `id`、带时区的 ISO 8601 `date`、非空 `tags` 列表、纯文本 `body` 与布尔 `draft`。为满足任务审阅元数据，样例还带 `title/type/source/created/status`。输出是可直接打开的 `preview.html`；生成器不读取仓库其他内容。

## 现状与差距

根 `_config.yml` 仅配置普通 posts、分页和 `jekyll-feed`，未声明短内容 collection；检索公开工程文件也未发现既有短内容或微博客页面。因此本薄切片复用 Markdown/frontmatter 概念，但隔离生成，不触碰生产站点。差距是尚未获得产品确认的 URL 命名、是否纳入主导航以及 RSS 策略。

## 首选最小方案与运行位置

首选在后续评审通过后增加 `_microblog` collection 与单个列表布局，保留当前生成器作为数据规则的参考校验器。页面可位于 `/microblog/`，条目使用 `/microblog/#<id>`，无需逐条生成页面。当前演示只运行在 `holiday-2026/A05-microblog-timeline/`。

## 兼容、成本与未知

最小生产补丁预计是根配置中的 collection 声明、一个隔离布局/页面和样式；本文不实施。旧文章 URL 完全不变。默认不把短内容加入现有 `/feed.atom`，从而保持 RSS 行为；若日后需要订阅，应新增 `/microblog/feed.atom`，不要改变旧 feed。成本主要是模板与可访问性复核。未知包括正式 URL、标签大小写规则、正文是否允许 Markdown、RSS 是否需要短内容。

## 失败恢复与退出路径

生成失败不会覆盖生产文件；命令返回非零。删除整个 A05 目录即可完全退出。若未来接入 Jekyll，回滚新增 collection、页面与布局即可恢复，旧 URL/RSS 不受影响。重复 ID、无时区日期或不合规字段必须先修数据再重跑，不静默跳过。

## 优先级

- **P0：**字段校验、重复 ID 拒绝、草稿默认隐藏、按绝对时间倒序且同时间按 ID 稳定排序、HTML/属性转义、标签筛选、锚点、空状态、移动端布局。
- **P1：**正式 Jekyll collection、独立 RSS、分页、Markdown body、构建期跨 collection 链接检查。

## 具体接受标准

1. 8 条合成样例均标注 DEMO，默认页面展示 7 条、草稿不展示。
2. 带不同时区的日期按绝对时间倒序；相同时间按 ID 升序。
3. 重复 ID、无时区日期返回退出码 2；不生成误导性成功结果。
4. 标签可筛选并可用 `#tag=` 恢复，零匹配显示空状态。
5. 每条有 `#<id>` 永久锚点；标签和正文 HTML 被转义。
6. 320px 及以上视口无需横向页面滚动，标签栏可独立横向滚动。
7. Python 标准库测试通过，生成文件可直接由浏览器打开。
8. 接入生产前由维护者决定 URL、导航与独立 RSS；生产构建通过后方可发布。
