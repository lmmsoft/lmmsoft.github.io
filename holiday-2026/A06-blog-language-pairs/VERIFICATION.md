---
title: "A06 博客多语言发布：验证记录"
type: verification
source: local-command-results
created: 2026-10-04
status: needs-review
tags:
  - tests
  - audit
---

# A06 博客多语言发布

## 实际执行

| 命令 | 最终退出码 | 测量结果 |
|---|---:|---|
| `python3 holiday-2026/A06-blog-language-pairs/language_pairs.py validate` | 0 | 1 组、2 份译稿有效；两份 effective status 均为 reviewed，publishable 均为 true。 |
| `python3 -m unittest discover -s holiday-2026/A06-blog-language-pairs/tests -v` | 0 | 运行 9 项测试，9 项通过；覆盖正常、缺失、重复、非法码、哈希漂移、unreviewed、代码块、链接和转义。 |
| `python3 holiday-2026/A06-blog-language-pairs/language_pairs.py build` | 0 | 生成 5 个 HTML：入口、review、zh-CN、en、zh-TW。 |
| 临时副本追加源文本后运行 `language_pairs.py validate --manifest <temp>/pairs.json` | 0 | 两份 declared reviewed 均自动变为 effective stale，publishable=false。stale 是有效但被阻断的状态，所以命令成功。 |
| 临时副本更新 revision/hash 并设 unreviewed 后再次校验 | 0 | 两份均为 unreviewed 且 publishable=false，证明可恢复同步而不会越过人工审阅。 |
| 临时副本将 zh-TW locale 改为 en 后再次校验 | 1 | 明确报告 duplicate locale 和 missing zh-TW；失败路径未被掩盖。 |
| `python3 -m py_compile holiday-2026/A06-blog-language-pairs/language_pairs.py holiday-2026/A06-blog-language-pairs/tests/test_language_pairs.py` | 0 | 两个 Python 文件语法编译通过。 |
| `git diff --check` | 0 | 无空白错误。 |

## 未执行与原因

- 未运行生产 Jekyll 构建：本任务按约束只在独立目录交付、不接入生产配置/布局/路由；生产构建无法证明该隔离工具的发布门禁，真正接入时必须在 Docker 中补跑。
- 未生成浏览器截图：环境未安装 `chromium`、`chromium-browser` 或 `google-chrome`。静态 HTML 已真实生成，可直接打开；这不等同于完成桌面/手机人工视觉验收。
- 未调用网络、翻译 API、部署或发布命令。

## 结论边界

本地合成三语流程、结构性对齐门禁、来源漂移和发布资格判断已由真实输出验证。语言自然度、生产 URL 契约选择、Jekyll 接入及跨设备视觉效果仍需人工 review，不能由上述测试代替。

## Local preservation review

- Re-ran 14 unit tests successfully and rebuilt all preview pages.
- Fixed index language links and per-page `lang` attributes.
- Rebuild preserves unrelated output files; unsafe group IDs, paths outside the manifest, content-directory outputs and output symlinks are rejected.
- Cloud percentages and elapsed time remain self-reported in the original run report; no production Jekyll or browser acceptance is claimed.
