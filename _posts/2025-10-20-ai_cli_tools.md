---
title:  "AI CLI 工具：Claude Code, Codex, Gemini CLI, Qwen code, CodeBuddy cli, cursor-agent 我的常用命令"
date: 2025-10-20T12:00:00+08:00
author: lmm333
layout: post
comments: true
published: true
permalink: /ai_cli_tools/
categories:
- 挨踢生涯
tags:
- AI
- 工具
- CLI
---

## 源起

今年的 AI CLI 工具特别火，尤其在编码等方面，Agent 技术大大提高了效率，可以闭环完成改代码、运行、验收测试、修复bug等任务的闭环，直到程序能正常工作，大大提升了vibe coding的效率。

我平时也几乎每天都在使用 Claude Code, Codex, Gemini CLI, Qwen code, CodeBuddy cli, cursor-agent 等 CLI 工具，来辅助我完成各种编程任务。

使用中有很多常用的命令，在不同 CLI 之间略有不同，这里整理一下，方便自己和大家参考：

## 更新版本

这些 cli 工具都在快速迭代，隔三差五都会有更新，我每天开机后都会运行下面的【一键检查版本+更新】的命令，获取最新的版本：

```sh
claude --version
codex --version
gemini --version
qwen --version
codebuddy --version
cursor-agent --version

npm install -g @anthropic-ai/claude-code
npm install -g @openai/codex
npm install -g @google/gemini-cli
npm install -g @tencent-ai/codebuddy-code 
npm install -g @qwen-code/qwen-code@latest
curl https://cursor.com/install -fsS | bash

claude --version
codex --version
gemini --version
qwen --version
codebuddy --version
cursor-agent --version
```

官方网站
- [Claude Code](https://www.claude.com/product/claude-code)
- [Codex](https://openai.com/zh-Hans-CN/codex/)
- [Gemini CLI](https://cloud.google.com/gemini/docs/codeassist/gemini-cli)
- [Qwen Code](https://qwenlm.github.io/qwen-code-docs/)
- [Qwen Code Doc](https://qwenlm.github.io/qwen-code-docs/zh/)
- [CodeBuddy](https://www.codebuddy.ai/)
- [Cursor CLI](https://cursor.com/cn/cli)

官方github：
- [Calude Code](https://github.com/anthropics/claude-code)
- [Codex](https://github.com/openai/codex/ )
- [Gemini CLI](https://github.com/google-gemini/gemini-cli)
- [Qwen Code](https://github.com/QwenLM/qwen-code)
- [CodeBuddy CLI](https://mp.weixin.qq.com/s/twmCoGDSr7Sv6UxQUBvRmg)

## 启动
直接使用 ```claude  codex  gemini qwen codebuddy cursor-agent``` 等命令就能启动。

但是默认启动参数，很多操作需要手动确认（eg: 修改代码，阅读外部目录，访问网络等），为了提高效率，我一般会使用 yolo 模式启动，省去确认环境，一把梭！

```shell
claude -dangerously-skip-permissions
codex --dangerously-bypass-approvals-and-sandbox 
gemini --yolo
qwen --yolo
codebuddy --dangerously-skip-permissions
```

## 启动快捷方式
上面的  yolo 模式启动参数太长了，我一般会写成别名，加到 .zshrc 里面，方便记忆和快速启动：

```sh
alias cl-yolo='claude -dangerously-skip-permissions'
alias co-yolo='codex --dangerously-bypass-approvals-and-sandbox'
alias ge-yolo='gemini --yolo'
alias qw-yolo='qwen --yolo'
alias cb-yolo='codebuddy --dangerously-skip-permissions'
```

## TBD 恢复对话

不同 cli 恢复对话的命令略有不同：

```sh
claude resume <conversation_id>
codex resume <conversation_id>
gemini resume <conversation_id>
qwen resume <conversation_id>
codebuddy resume <conversation_id>
```

## MCP
MCP 技术，让大模型能和外部的工具更好地结合起来，完成更复杂的任务。

查询 mcp 状态
```shell
claude mcp list
codex mcp list
gemini mcp list
qwen mcp list
```

### Playwright MCP
我平时使用最多的 mcp 是  playwright mcp, 用来做浏览器自动化的，几乎可以帮我完成大部分 UI Automation 的任务， 比如改了一个功能，让AI自动在网页上点点鼠标，验收测试的场景。

下面是不同 cli 安装 playwright mcp 的命令：

```sh
claude mcp add playwright npx @playwright/mcp@latest
codex mcp add playwright npx @playwright/mcp@latest
gemini mcp add playwright npx @playwright/mcp@latest
qwen mcp add playwright npx @playwright/mcp@latest
```

参考文档：
- [Playwright](https://playwright.dev/)
- [Playwright mcp](http://github.com/microsoft/playwright-mcp)
- [codex mcp](https://github.com/openai/codex/blob/main/docs/config.md#mcp_servers )

### Context7 MCP
据说这个 MCP 有很多文档，可以提高 AI 写代码调用接口的能力

```shell
claude mcp add context7 -- npx -y @upstash/context7-mcp
```

参考文档
- [lobehub Context7 MCP](https://lobehub.com/zh/mcp/upstash-context7)
