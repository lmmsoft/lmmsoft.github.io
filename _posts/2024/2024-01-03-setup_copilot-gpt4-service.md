---
title:  "搭建 copilot-gpt4-service"
date: 2024-01-31T00:00:00+08:00
author: lmm333
layout: post
comments: true
published: true
permalink: /setup_copilot-gpt4-service/
categories:
- 挨踢生涯
tags:
- GPT-4
- copilot
- next
---
## 一句话总结
昨晚使用 github 上的开源项目 https://github.com/aaamoon/copilot-gpt4-service 搭建了可以白嫖 gpt4 的代理，分享一下搭建过程。

## 背景
前置条件是需要有一个 github copilot 账号。这是 github 基于 GPT4 模型辅助写代码的工具，还有 VSCode, IntelliJ 插件，一般 github pro 的付费用户，教育用户，深度开源用户会有 github copilot 功能。我恰好有，所以可以继续。

## 插件原理
github copilot 插件原理是通过将代码与上下文发送到 github copilot 服务器，然后调用 gpt3.5/4的模型，返回结果，辅助写代码。

这个开源项目的原理类似，通过拿到 github copilot api的授权，然后代理转发 api，就可以实现白嫖 gpt4 的效果。

## 搭建大致流程

（ps: 项目已过期，这里省略若干字）

## 其他注意事项
- Github Copilot 只支持 GPT-4 和 GPT-3.5-turbo模型。如果选了 gpt-4-32k-0613 模型，实际上是在用 GPT-3.5-turbo 模型 [ref](https://github.com/aaamoon/copilot-gpt4-service/issues/254)

## 参考链接🔗
- copilot-gpt4-service 项目地址 https://github.com/aaamoon/copilot-gpt4-service
- copilot-gpt4-service 中文文档 https://github.com/aaamoon/copilot-gpt4-service?tab=readme-ov-file
- NextChat 项目地址 https://github.com/ChatGPTNextWeb/ChatGPT-Next-Web/
- NextChat 中文文档 https://github.com/ChatGPTNextWeb/ChatGPT-Next-Web/blob/main/README_CN.md