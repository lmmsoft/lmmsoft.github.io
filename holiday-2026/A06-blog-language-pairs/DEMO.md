---
title: "A06 博客多语言发布：合成数据演示"
type: demo
source: synthetic-demo
created: 2026-10-04
status: needs-review
tags:
  - multilingual
  - static-preview
---

# A06 博客多语言发布

## 数据声明

本目录的文章、英文译稿和繁体译稿全部是为本任务自行撰写、人工编辑的 **synthetic（合成）公开安全演示数据**。它们不代表真实业务内容、真实发布或生产接入成果，也不是机械字形转换结果。未调用翻译 API。

## 演示路径

1. 运行 `python3 holiday-2026/A06-blog-language-pairs/language_pairs.py build`。
2. 直接打开 `holiday-2026/A06-blog-language-pairs/site/index.html`，或在仓库根运行 `python3 -m http.server 8000 --bind 127.0.0.1 --directory holiday-2026/A06-blog-language-pairs/site`。
3. 从首页进入任一语言，以页首 `zh-CN / en / zh-TW` 切换。
4. 打开“差异审阅”，确认 declared/effective status、来源哈希和发布资格。
5. 在源稿末尾加一行但不更新清单，再跑 `validate`；两份译稿会变成 stale、publishable 为 false。恢复源稿即可恢复，无需发布或回滚站点。

## 能看到什么

- 三种人工措辞，而非简繁字符替换。
- 三份稿件完全相同的 shell 代码、URL、`Cache-Control` 与 GitHub Pages 专名。
- 带合成数据标记的隔离预览。
- 审阅状态门禁；这里只证明工具行为，不声称语义审阅已在真实流程中完成。
