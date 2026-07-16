---
title: "模仿陶哲轩，我也在博客上创建了个人旅行记录页"
date: 2026-07-16T12:00:00+08:00
author: lmm333
layout: post
comments: true
published: true
permalink: /personal-travel-page-inspired-by-terence-tao/
categories:
- 挨踢生涯
tags:
- AI
- Jekyll
- 博客
- 旅行
- Vercel
- GitHub Pages
---

最近看到陶哲轩博客上的 [Travel 页面](https://teorth.github.io/tao-web/travel.html)，觉得这种“时间轴 + 坐标 + 链接”的记录方式很好：年份、日期和地点排在一起，再关联到对应的文章，既能回顾一个人的移动轨迹，也比在几百篇博客文章里翻游记方便得多。

于是我也让 AI 帮我调研、设计和实现了一版自己的[旅行记录页](/travel/)。

<!--more-->

## 从陶哲轩的 Travel 页面得到启发

陶哲轩的 Travel 页面并不花哨。它没有地图、动画和复杂筛选，主体就是按年份排列的行程记录。但正是这种克制，让信息非常容易浏览：想看某一年去了哪里，沿着时间轴往下找就可以。

![陶哲轩的 Travel 页面：按年份排列未来行程与历史行程](/images/2026/2026-07-16-personal-travel-page-inspired-by-terence-tao/tao-travel-page.jpg)

*陶哲轩的 Travel 页面：极简的年份、日期与地点时间轴。*

我以前的旅行记录散落在博客游记、年度清单和其他个人记录中。单篇文章适合讲故事，却不适合回答这些问题：

- 某一年去过哪些城市？
- 同一次旅行写了几篇文章？
- 某个博物馆是哪次行程去的？
- 十几年间，自己的活动范围发生了什么变化？

所以我真正想模仿的不是页面样式，而是把时间、坐标和文章链接组织成一份长期可维护的数据。

## 第一步：让 AI 调研他的实现

陶哲轩的网站仓库 [tao-web](https://github.com/teorth/tao-web) 公开可读，成品页面和实现代码可以互相对照。需要说明的是，仓库公开可读不等于所有内容都可以随意复制；我的做法是研究架构思路，然后在自己的博客里独立实现。

AI 顺着页面找到了几处关键代码：

- 行程数据维护在 [`data/travel/travel.yaml`](https://github.com/teorth/tao-web/blob/main/data/travel/travel.yaml)；
- [`travel.schema.json`](https://github.com/teorth/tao-web/blob/main/schema/travel.schema.json) 负责约束数据格式；
- [`scripts/build.py`](https://github.com/teorth/tao-web/blob/main/scripts/build.py) 在构建时生成静态 HTML；
- [GitHub Actions](https://github.com/teorth/tao-web/blob/main/.github/workflows/deploy.yml) 完成校验、构建并发布到 GitHub Pages。

整体链路可以简化为：

```text
travel.yaml → Schema 校验 → Python 构建 → 静态 HTML → GitHub Pages
```

浏览器并不会在打开页面时再请求 YAML，也没有为了这张旅行清单启动后端服务。所有工作都在构建阶段完成，最终仍然是一张简单、稳定、容易缓存的静态网页。

这次调研让我确定了三个原则：

1. 旅行数据和页面展示应该分开；
2. 最终页面应该继续保持纯静态；
3. 数据要有明确规则，不能靠一大段 HTML 手工维护。

## 第二步：结合自己的 Jekyll 博客设计方案

我的博客本来就是 Jekyll，没有必要照搬陶哲轩的 Python 构建脚本，更没必要为了一个页面增加新的技术栈。

最后采用的是 Jekyll 原生方案：

```text
_data/travel.yml + Liquid 模板 + 文章 travel_id → /travel/ 静态页面
```

![我的博客旅行记录页：年份、旅行主题、城市、地点与文章链接](/images/2026/2026-07-16-personal-travel-page-inspired-by-terence-tao/lmmsoft-travel-page.jpg)

*我的旅行记录页：在时间轴上补充旅行主题、地点和相关文章。*

公开行程统一维护在 [`_data/travel.yml`](https://github.com/lmmsoft/lmmsoft.github.io/blob/master/_data/travel.yml)，每条记录包含年份、日期、城市、地点或景点，以及可选的旅行主题：

```yaml
- year: 2025
  trips:
    - id: 2025-01-25-spring-road-trip
      date: "01-25~02-03"
      title: "春节粤西自驾"
      place: "深圳、阳江、钦州、南宁、茂名、开平、江门、顺德、东莞、香港"
      spots: [海陵岛, 广西壮族自治区博物馆, 茂名博物馆, 开平碉楼]
```

游记本身不需要把链接重复写进 YAML，只要在文章 frontmatter 中声明同一个 `travel_id`：

```yaml
travel_id: 2025-01-25-spring-road-trip
```

构建时，[`f_travel.md`](https://github.com/lmmsoft/lmmsoft.github.io/blob/master/f_travel.md) 会自动找到这些文章，并在对应行程下面生成站内链接。这样新增游记时只维护关联关系，不需要同时修改旅行页上的 URL。

我还做了一个与陶哲轩不同的选择：默认只公开已经发生并经过确认的行程，不公开未来的具体旅行计划。技术可以自动化，隐私边界不能跟着自动化一起消失。

## 第三步：让 AI 实现，再一版一版打磨

第一版很快就跑起来了，但“能显示”距离“好用”还差得很远。

最早整理出来的记录主要集中在近几年。我继续追问：2024 年以前真的没有旅行吗？AI 又回头检查早期博客文章和清单，补齐了 2008、2009、2012 以及 2014 年之后的记录。

之后又调整了很多细节：

- 连续多天属于同一次出行的，不再按每天拆开，而是聚合成日期范围；
- 国内行程写城市，境外行程使用“国家-城市”；
- 增加旅行主题字段，比如为多日行程补充“春节粤西自驾”“新西兰自驾”等主题，让人更容易理解这段旅程；
- 同一次行程的多篇游记集中在一起，并且每篇文章独占一行；
- 增加年份导航，并为手机端调整成更适合阅读的单栏布局。

最终页面收录了 16 个年份、112 段行程、397 条地点记录，并关联了 60 篇已经发布的文章。数据量不算巨大，但已经足够让我从另一个角度重新看到过去十几年的生活。

页面上线后，我又沿用同一套预览流程继续准备第二轮优化：让相关文章按照日期正序排列、手机端默认收起文章导航，并在顶部自动展示统计摘要。每一项仍然先进入 Vercel 预览站点验证，再决定是否合并到正式网站。

## 当 CI/CD 接上 AI：从提交到验证的自动反馈闭环

这次真正让我觉得好用的，不只是 AI 能写代码，而是 Codex、GitHub 和 Vercel 串成了一条能够自动构建、检查和修正的反馈链路：

```text
Codex 创建 Git 分支并修改代码
  → 提交 GitHub Pull Request
  → Vercel 自动生成预览站点
  → Codex 在桌面和手机尺寸检查 UI 效果
  → Codex 根据检查结果继续修改并推送
  → Vercel 自动生成新预览
  → Codex 重新验证，直到问题收敛
  → 检查通过后进入待合并状态
  → 人工决定是否合并到 master
  → GitHub Pages 发布正式网站
```

每次 Codex 把改动推送到 GitHub 后，Vercel 都会为这个 PR 创建独立预览地址。Codex 不再只看本地源码猜测效果，而是直接读取真实构建出来的网页，把部署结果作为下一轮修改的反馈。

页面太窄、相关文章挤成一团、导航在手机上遮挡正文，这些问题都能在预览页里立即发现。Codex 可以打开预览页面、读取 DOM、切换桌面和手机视口、操作导航按钮，并检查有没有横向溢出；发现问题后，它会继续修改代码、推送并等待下一轮 Vercel 构建。

这条链路的关键不是堆了多少工具，而是反馈重新回到了 AI 手里。常规的实现、部署、UI 检查和修复可以自动闭环，不需要我逐步确认；我只需要在最后保留“是否公开发布”这道人为闸门。

## AI 加速实现，人来决定什么值得公开

这次 AI 做了很多工作：调研开源实现、扫描旧文章、整理候选行程、设计数据结构、修改 Jekyll 模板、创建 PR，以及在 Vercel 预览页验证效果。

但真正需要人来判断的事情并没有消失：

- 哪些相邻记录属于同一次旅行？
- 一个普通周末出门算不算旅行？
- 没有游记的行程要不要展示？
- 哪些地点信息适合公开？
- 页面应该继续保持简单，还是加入地图和更多交互？

AI 很擅长从散落的信息中寻找关联，也很适合承担重复的实现和验证工作；但页面最后表达什么、公开到什么程度，仍然应该由自己决定。

现在，这张[个人旅行记录页](/travel/)已经成为博客里的一个长期入口。以后每写一篇新游记，只要补充对应的行程和 `travel_id`，它就会自动进入这条不断延伸的时间轴。

本文对陶哲轩网站实现的调研基于 2026-07-15 可见的公开仓库内容。
