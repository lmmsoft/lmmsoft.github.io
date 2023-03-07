---
title:  "Page View in static page"
date: 2000-00-00T00:00:00+08:00
author: lmm333
layout: post
comments: true
published: false
permalink: /link_xxx/
categories:
- x
tags:
- a
- b
---

最近给我的博客和Github主页添加了计数器，介绍一下相关的工具和技术。

# 博客
- 使用的是 卜算子

# Github主页
- 使用的是 visitor-badge
  - 项目源码 https://github.com/jwenjian/visitor-badge
- 作者介绍该工具的博客
  - https://medium.com/@1link.fun/the-story-of-visitor-badge-1bded5ed56b4
- TLDR
  - 使用 svg 动态生成图片
  - 后端搭建在免费版本的 glitch.com 
  - 没有自己建数据库，还是使用 https://countapi.xyz/ 提供的计数API
  - 作者推荐了类似工具： 
    - Hits
      - 项目主页 https://github.com/dwyl/hits
    - plantree visitor-badge
      - 项目介绍 https://plantree.github.io/project-docs/visitor-badge/introduction.html
      - 使用 https://github.com/plantree/counter 做统计