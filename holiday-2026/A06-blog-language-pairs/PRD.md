---
title: "A06 博客多语言发布：最小产品需求"
type: prd
source: repository-review-and-synthetic-design
created: 2026-10-04
status: needs-review
tags:
  - multilingual
  - validation
---

# A06 博客多语言发布

## 目标

让一篇中文源稿拥有可人工审阅的英文和繁体中文版本，以稳定 `translation_group_id` 配对，用来源版本和 SHA-256 追踪变化；译稿在来源变化后自动呈现为 `stale`，`stale` 或 `unreviewed` 永远不能取得 `publishable: true`。交付物只生成隔离的本地静态预览，不修改、不部署生产站点。

## 输入与输出

- 输入：`pairs.json` 清单和三份带 YAML frontmatter 的公开安全合成 Markdown；`zh-CN` 是源语言，`en`、`zh-TW` 是人工编辑演示稿。
- 输出：校验 JSON、非零失败退出码，以及 `site/index.html`、三语页面和 `site/review.html`。
- 不输入：私人知识库、身份资料、凭据、真实家庭/学校/健康/工作素材。

## 现状与差距

仓库 `_config.yml` 的 `locale: en_US` 仅供页面元数据使用，而 `default_locale: cn` 和 `locales` 是主题界面词典；现有 `_includes/head.html` 只输出当前页面 canonical 和单个 Atom feed。文章未见语言配对字段、来源哈希、审阅状态、hreflang 或按语言 feed。生产路由主要由各页 frontmatter 和 Jekyll 默认文章规则决定；项目规则要求英文 slug 尽量与 permalink 一致。

差距是内容级 locale 与界面 locale 混在一起、没有稳定配对索引、没有来源漂移门禁，也没有差异审阅面。此次不碰生产配置、布局、正文与路由。

## 首选最小方案

1. 使用可版本控制的 JSON 清单，不增加 Ruby/Python 包。
2. 源稿全文件字节计算 SHA-256；清单同时存 `source_revision` 和 `source_hash`。
3. 校验器动态计算 `effective_status`：哈希或 revision 不匹配即为 `stale`，无论声明为何；只有有效状态为 `reviewed` 的译稿可发布。
4. 完整性门禁覆盖缺语言、重复 locale、非法语言码、代码块、链接目标、行内代码、GitHub Pages 专名和引用数量；语义质量明确留给人工审阅。
5. 构建物写入任务目录的 `site/`，以明显的 synthetic / 不发布提示、语言切换和 review 页面呈现。

## 运行位置

从仓库根目录运行：

```bash
python3 holiday-2026/A06-blog-language-pairs/language_pairs.py validate
python3 holiday-2026/A06-blog-language-pairs/language_pairs.py build
python3 -m http.server 8000 --bind 127.0.0.1 --directory holiday-2026/A06-blog-language-pairs/site
```

然后打开 `http://127.0.0.1:8000/`。最后一条只提供本机文件，不是部署。

## 成本、未知与失败恢复

- 成本：仅 Python 标准库和静态文件，无付费翻译 API、托管费或后台服务。
- 未知：生产 URL 迁移策略、历史文章的语言归属、译者/审核人责任、RSS 消费者兼容数据尚未确定。
- 失败恢复：校验失败不会生成新站点；修正清单/内容后重跑。若源稿有意变化，先增加 `source_revision`，人工同步每份译稿，再用当前哈希更新清单并将状态从 `unreviewed` 改成 `reviewed`。可删除 `site/` 后重新构建，源文件不受影响。

## 优先级

### P0

- 稳定组 ID、严格 locale 唯一性和三语完整性。
- 来源 revision/hash 漂移自动 stale。
- stale/unreviewed 发布阻断。
- 代码块、链接、行内代码、专名、引用保护。
- 隔离的三语静态预览、切换与 review 页面。

### P1

- 接入 Jekyll collection/data、页面级 hreflang/canonical、语言 feed。
- 更精细的段落对齐和可签名审阅记录。
- 对历史内容进行人工盘点与渐进迁移。

## 验收标准（12 项）

1. 正常三语样例校验成功。
2. 缺译稿失败。
3. 重复 locale 失败。
4. 非法语言码失败。
5. 来源哈希变化后两份译稿自动 stale。
6. stale 不可发布。
7. unreviewed 不可发布。
8. 代码块变化失败。
9. 链接目标变化失败。
10. URL 属性安全转义。
11. 本地生成三语切换与差异 review 页面。
12. 对生产 hreflang/canonical/RSS/URL 接入给出明确但未执行的契约。
