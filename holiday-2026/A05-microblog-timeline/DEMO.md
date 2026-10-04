---
title: "A05 短内容／微博客时间流 — DEMO"
type: demo-guide
source: synthetic
created: 2026-10-04
status: needs-review
tags: [A05, microblog, synthetic]
---

# A05 短内容／微博客时间流

本演示中的 8 条内容全部是为界面验证原创的**合成数据（synthetic DEMO）**，不对应真实人物、地点、账号、事件或业务发布。生成成功只代表本地静态薄切片成功，并不代表生产接入完成。

## 运行

```bash
cd holiday-2026/A05-microblog-timeline
python3 generate.py
python3 -m http.server 8000 --bind 127.0.0.1
```

浏览 `http://127.0.0.1:8000/preview.html`。也可直接打开 `preview.html`。点击标签进行筛选，点击时间旁的 `#` 获取条目锚点。默认隐藏 `demo-draft`；审阅草稿行为可另生成临时文件：

```bash
python3 generate.py --include-drafts --output /tmp/a05-with-drafts.html
```
