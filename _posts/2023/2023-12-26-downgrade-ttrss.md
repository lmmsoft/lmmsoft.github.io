---
title:  "降级 tiny tiny RSS 镜像版本，解决 Awesome-TTRSS 部署问题"
date: 2023-12-26T12:00:00+08:00
author: lmm333
layout: post
comments: true
published: true
permalink: /downgrade_ttrss/
categories:
- 挨踢生涯
tags:
- ttrss
- rss
---

## 一句话总结

今年开始自己部署 ttrss 作为 RSS 阅读器，使用的是 [HenryQW/Awesome-TTRSS](https://github.com/HenryQW/Awesome-TTRSS) 的  Tiny Tiny RSS(一款基于 PHP 的免费开源 RSS 聚合阅读器) + opencc(繁体中文转简体) + mercury(抓取全文) 的一站式容器方案，今天降级了 ttrss 的版本，解决了2个部署问题。

<!--more-->

## 两个问题

### 1. mercury-parser-api 无法使用
mercury api 是用来抓取全文的，很多rss只提供了标题/摘要，没有全文，这个api可以抓取全文。但在我使用半年前的版本部署时，这个api无法使用，

我提过 [issue1](https://github.com/HenryQW/mercury_fulltext/issues/28) [issue2](https://github.com/HenryQW/Awesome-TTRSS/issues/460) 但是一直没人回复，我也没找到解决方案，不影响核心功能使用，就一直放着了。


### 2. 升级最新版，数据库迁移失败，无法使用
这个问题 github issue 里面[也有](https://github.com/HenryQW/Awesome-TTRSS/issues/463)，暂无人解决，我也遇到了一样的问题。

## 解决方案
今天升级了最新版，结果数据库迁移失败，完全无法使用，就必须修复了。

经过尝试，最后的解决方案是，降级到年初的版本，这个版本不需要迁移数据库 schema，mercury api 也可以正常使用。

```shell
docker pull wangqiru/ttrss:nightly-2023-01-01
```
然后修改 [docker-compose.yml](https://github.com/HenryQW/Awesome-TTRSS/blob/main/docker-compose.yml) 文件即可，mercury 和 opencc 的镜像不需要改，很久也没更新了，保持 latest就可以。

```dockerfile
version: "3"
services:
  service.rss:
    image: wangqiru/ttrss:nightly-2023-01-01
    container_name: ttrss
    ...
```

## 其他
今天顺带把部署机从 Azure 的 1核1G 虚拟机换到了群晖 NAS 上，pg数据库还保持在 Azure 上。

1核的机器太卡了，打开一个博客要等十几秒，而且经常超时，换到 NAS 上，速度快了很多。