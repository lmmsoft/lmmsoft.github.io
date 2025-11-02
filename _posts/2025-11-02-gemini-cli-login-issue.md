---
title: "Gemini CLI 登录踩坑记录：GOOGLE_CLOUD_PROJECT_ID 的坑与解法"
date: 2025-11-02T00:00:00+08:00
author: lmm333
layout: post
comments: true
published: true
permalink: /gemini-cli-login-issue/
categories:
  - 挨踢生涯
tags:
  - Gemini
  - CLI
  - Google Cloud
---
## 一句话总结
Gemini CLI 升级后出现强制重新登录的流程，但在主力 Google 账号上始终触发 `This account requires setting the GOOGLE_CLOUD_PROJECT or GOOGLE_CLOUD_PROJECT_ID env var` 错误，经过一轮排查与尝试，最终确认这与旧的 Google Cloud 项目绑定有关，改用未启用 Gemini API 的账号即可无痛登录。

<!--more-->

## 背景

过去几个月我一直用 Gemini CLI 写代码、发起快速问答，体验稳定。两天前升级到最新版后，命令行提示需要重新登录。照着提示打开浏览器，在 Google 的授权页面完成 OAuth 流程，回调页面显示 `Login successful`，看起来一切正常（参考官方成功回调页面示意 [auth_success_gemini](https://developers.google.com/gemini-code-assist/auth/auth_success_gemini?hl=zh-cn)）。

然而 CLI 这边随即抛出错误：

```
Failed to login. Message: This account requires setting the GOOGLE_CLOUD_PROJECT or GOOGLE_CLOUD_PROJECT_ID env var. See https://goo.gle/gemini-cli-auth-docs#workspace-gca
```

重复多次依旧失败，说明问题发生在本地 CLI 与账户的后续校验阶段。

## 排查过程

1. **确认是不是官方已知问题。** 翻了下官方 GitHub 仓库 [google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli)，issue 区确实有人反馈同样的报错，维护者在 [#3001](https://github.com/google-gemini/gemini-cli/issues/3001) 建议设置 `GOOGLE_CLOUD_PROJECT_ID` 环境变量。
2. **尝试官方论坛建议。** 官方支持论坛也有一则 [讨论串](https://support.google.com/gemini/thread/353383847/gemini-cli-login-issue?hl=en) 建议删除主目录下的 `.gemini` 配置重新初始化。实际操作后完全无效，CLI 仍然报同样的错，可视为误导信息。
3. **社区经验搜索。** Twitter/X 上不少开发者抱怨（例如 [@imvihv](https://x.com/imvihv/status/1937885189168070911)、[@kiwiflysky](https://x.com/kiwiflysky/status/1937884993709363232)）登录失败与 Workspace 账号限制、项目绑定有关。

综合来看，问题并非本地缓存，而是和 Google Cloud 项目绑定状态强相关。

## 临时可用但副作用巨大的方案

按照 issue #3001 的建议，登录前先在终端导出项目 ID：

```shell
export GOOGLE_CLOUD_PROJECT_ID=gen-lang-client-0698601424
```

项目 ID 可以在 Google Cloud 控制台的欢迎页面看到（控制台首页右上角的“项目 ID”字段，示例可参考下方 Google Cloud Console 链接）。

随后再执行 `gemini login`，确实可以通过验证。

但现实里这个方案有三个明显缺点：

- **环境变量不持久。** 每次重启终端都要重新 `export`，除非写进 `~/.bashrc` 或 `~/.zshrc`，使用体验很差。
- **需要启用 Gemini API。** 只有在 Google Cloud 项目中为账号启用了 Gemini API 后，CLI 才能继续调用，这一步有可能触发计费。一些网友反馈开启后免费额度失效，每日 200 次 Pro 模型额度和 Flash 免费调用都会被记入项目账单。
- **账单风险不透明。** 我的账号是在之前测试 Vertex AI 时自动生成的项目，没有设置付款方式，所以暂时没有被扣费；但一旦绑定信用卡，后续费用就不再可控。

综上，这个方法只是权宜之计，风险远大于收益。

## 最终的稳定方案：更换 Google 账号

在排除环境变量方案之后，我尝试使用一个从未在 Google Cloud 开通过 Gemini 项目的个人账号重新登录：

1. 退出 CLI：`gemini logout`，并清理 `~/.gemini` 目录。
2. 使用备用 Google 账号在浏览器完成 OAuth 授权。
3. 回到终端执行 `gemini login`，这次没有再提示设置项目 ID，直接进入可用状态。

实测表明，只要账号没有绑定旧的 Gemini API 或 Workspace 限制，登录流程就和旧版本一样顺利。对于需要继续使用主力账号的同学，目前还没有官方给出的无风险修复，需要等待 CLI 后续更新。

## 小结

- 触发 `GOOGLE_CLOUD_PROJECT_ID` 报错的根源在于旧项目或 Workspace 限制，而非本地缓存。
- 通过导出 `GOOGLE_CLOUD_PROJECT_ID` 可以临时登录，但需要启用 Gemini API，可能带来计费与额度损失。
- 更换一个未启用 Gemini API 的 Google 账号是现阶段最稳妥的解决方案。

如果你也遇到相同问题，建议先确认自己是否在 Google Cloud 中启用了相关项目，再决定是承担计费风险继续使用，还是临时更换账号等待官方修复。

## 参考链接

- [Gemini CLI 登录成功回调页示例](https://developers.google.com/gemini-code-assist/auth/auth_success_gemini?hl=zh-cn)
- [Gemini CLI 官方仓库](https://github.com/google-gemini/gemini-cli)
- [Issue #3001: Gemini CLI login requires GOOGLE_CLOUD_PROJECT_ID](https://github.com/google-gemini/gemini-cli/issues/3001)
- [Google 支持论坛：Gemini CLI login issue](https://support.google.com/gemini/thread/353383847/gemini-cli-login-issue?hl=en)
- [Google Cloud Console 项目示例（需登录）](https://console.cloud.google.com/welcome?project=gen-lang-client-0698601424)
- [X 上的社区讨论 1](https://x.com/imvihv/status/1937885189168070911)
- [X 上的社区讨论 2](https://x.com/kiwiflysky/status/1937884993709363232)
