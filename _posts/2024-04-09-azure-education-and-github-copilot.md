---
layout: post
title: "学生身份申请 Azure 和 GitHub Copilot 的避坑指南"
date: 2024-04-09 09:00:00 +0800
author: lmm333
comments: true
permalink: /azure-education-and-github-copilot/
categories:
  - 挨踢生涯
tags:
  - Azure
  - GitHub
  - Copilot
  - 教育优惠
---

一直听朋友说“学生身份真香”，直到真正操作一遍，才发现微软和 GitHub 的教育福利流程里还有不少细节。本文把申请 Azure for Students、GitHub Student Developer Pack 以及启用 Copilot 的关键步骤整理成册，少走弯路。

<!--more-->

## 先准备好学生身份材料

两大平台都会校验学校邮箱，因此第一步就是确认自己仍然能访问学校提供的邮箱。如果学校没有开放邮件服务，也可以准备在读证明或学生证照片，后续人工审核会用到。

我自己的流程是：

1. 登录学校统一认证平台，确认邮箱仍然可以转发邮件。
2. 预先截取学生证或学籍页面，遇到人工验证时能迅速上传。

## Azure for Students 开通步骤

1. 访问 [Azure for Students](https://azure.microsoft.com/zh-cn/free/students/) 页面，用学校邮箱注册微软账户。
2. 按照提示填写基本信息，注意国家/地区必须和校园所在地区一致。
3. 验证方式里可以选择银行卡或者手机号。我用的是国内手机号，验证码秒到。
4. 完成验证后，Azure 会在订阅里新增 `Azure for Students`，提供 100 美元额度和部分免费服务。

首批额度主要用来部署测试环境，比如开个 B1S 虚拟机、搭个 PostgreSQL Server，非常够用。记得在门户里设置消费警报，避免误开付费实例。

## GitHub Student Developer Pack + Copilot

1. 打开 [GitHub Student Developer Pack](https://education.github.com/pack)，点击 `Get benefits`。
2. GitHub 会要求绑定学校邮箱，可以使用和 Azure 相同的邮箱，之后提交学生证或在读证明。
3. 审核通过后就能获得包含 Copilot 在内的大礼包。我在收到通过邮件后，前往 [GitHub Copilot](https://github.com/features/copilot) 页面启用即可。

Copilot 默认会绑定到所有支持的 IDE，包括 VS Code、JetBrains 系列以及命令行。为了避免误用团队配额，建议在 `Settings > Copilot > Policies` 中开启 “Allow or block specific organizations” 的限制。

## 常见问题

- **审核迟迟不通过**：Azure 和 GitHub 都支持重新提交材料。多提供几张不同角度的学生证照片通常能加快处理速度。
- **学校邮箱收不到验证码**：可以先把 `@microsoft.com`、`@github.com` 加入白名单，必要时使用备用邮箱再申请一次。
- **Copilot 仍然显示试用版**：退出 GitHub 账号重新登录 IDE，或者在浏览器端关闭再开启 Copilot 授权，多数情况下就能刷新到教育版权益。

## 结语

学生折扣是学习和实践的最佳加速器。申请流程做一次记录，之后帮朋友开通时也能直接照着步骤来，不用再在邮件往返里消耗时间。
