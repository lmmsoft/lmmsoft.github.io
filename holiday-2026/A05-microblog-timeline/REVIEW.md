---
title: "A05 短内容／微博客时间流 — Review"
type: review
source: implementation-review
created: 2026-10-04
status: needs-review
tags: [A05, review, microblog]
---

# A05 短内容／微博客时间流

## 审阅重点

- 数据契约是否接受 `body` 位于 frontmatter、标签区分大小写，以及同时间按 ID 排序。
- 正式接入是否采用 `_microblog` collection 与 `/microblog/#id`。
- 是否继续让旧 `/feed.atom` 只含长文；如需要短内容，是否接受独立 feed。
- 移动端标签栏、焦点行为、颜色对比与空状态文案。

## 已完成边界

隔离目录内已有无依赖生成器、8 条合成输入、静态预览和聚焦测试。未改根配置、生产导航、RSS 或已发布文章；未部署，也未声称完成真实业务验收。

## 建议评审决定

通过数据规则与交互后，再以小补丁接入 Jekyll。若拒绝此模型，直接删除本目录即可，无数据迁移或 URL 清理成本。
