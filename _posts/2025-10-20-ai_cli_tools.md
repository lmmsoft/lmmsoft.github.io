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

我平时也几乎每天都在使用 Claude Code, Codex, Gemini CLI, Qwen code, CodeBuddy cli, cursor-agent 等 CLI 工具，来辅助我完成各种编程任务，**大大扩展了我的能力边界，也提高了我的开发速度，有种代码写得太快，来不及review的感觉**。

使用中有很多常用的命令，在不同 CLI 之间略有不同，这里整理一下，方便自己和大家参考：

<!--more-->

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
cursor-agent --force
```

## 启动快捷方式
上面的  yolo 模式启动参数太长了，我一般会写成别名，加到 .zshrc 里面，方便记忆和快速启动：

```sh
alias cc='claude -dangerously-skip-permissions'
alias cx='codex --dangerously-bypass-approvals-and-sandbox'
alias ge='gemini --yolo'
alias qw='qwen --yolo'
alias cb='codebuddy --dangerously-skip-permissions'
alias cu='cursor-agent --force'
```

## 配置文档 AGENTS.md
各种 llm cli 都有自己的 .md 配置文件，类似于Cursor的Rules文件，规定了AI怎样生成代码，可以在里面指定代码风格、开发环境、仓库规范等等。 文件会作为上下文，一起发送给大模型，帮助理解项目，规范输出。

一般会可以在全局，根目录，子目录等多个位置放置 .md 的配置文件。用户 prompt 优先级最高，然后离编辑文件越近的 .md 文件优先级越高。

### 统一的 AGENTS.md
不同 llm 都有自己的 .md 文件，一般可以使用 /init 命令自动生成，如果一个项目同时使用多个 cli 开发， .md 文件的差异比较麻烦，目前 openai 提出了统一的 AGENTS.md 方案，统一了部分cli， 详情可以参考文档 [agents.md](https://agents.md/)

我常用的 codex/cursor/gemini cli/warp 都支持

Gemini CLI 需要特殊配置一下 .gemini/settings.json 文件：

```json
{ "contextFileName": "AGENTS.md" }
```

gemini 系的 cli 应该都能使用这个参数，比如 qwen code 也支持， [参考文档](https://qwenlm.github.io/qwen-code-docs/zh/cli/configuration-v1/#settingsjson-%E4%B8%AD%E5%8F%AF%E7%94%A8%E7%9A%84%E9%85%8D%E7%BD%AE%E9%A1%B9)

### 其他语言
- claude
  - claude 使用 claude.md （推荐提交到代码仓库，团队共享） 和 claude.local.md （推荐加入 .gitignore 个人使用，比如开发环境的配置）
  - claude.md 有四种位置
    - 企业策略: eg: Linux: /etc/claude-code/CLAUDE.md 公司编码标准、安全策略、合规要求
    - 项目：./CLAUDE.md 项目架构、编码标准、常见工作流程
    - 个人：~/.claude/CLAUDE.md 代码样式偏好、个人工具快捷方式
    - 项目内个人: ./CLAUDE.local.md （已弃用，建议用"引用其他文件"） 沙盒 URL、首选测试数据
  - 引用其他文件：CLAUDE.md 文件可以使用 @path/to/import 语法导入其他文件
  - 详情参考 https://docs.claude.com/zh-CN/docs/claude-code/memory
- cursor
  - 同时兼容
    - cursor IDE 的 rule 目录： .cursor/rules
    - codex 的 AGENTS.md
    - claude 的 CLAUDE.md
  - rules 文档 https://cursor.com/docs/context/rules
  - cli 文档 https://cursor.com/cn/docs/cli/using#-1


### 我的常用 .md 配置

- 全局配置：
```markdown
用中文回答我
每次对用审视的目光，仔细看我输入的潜在问题，你要指出我的问题，并给出明显在我思考框架之外的建议
如果你觉得我说得太离谱了，你就骂回来，帮我瞬间清醒
```

- 项目配置：
  - 如果是 python 项目，会告诉它虚拟环境 venv 的目录在哪里，如何启动，方便它在虚拟环境里运行程序

claude.md/gemini.md/agents.md 

## 配置文件
类似于 setting.json, 这个用的不多，简单记录：

- claude code
  - `~/.claude/settings.json`
  - 全局，项目，企业 级别
  - https://docs.claude.com/en/docs/claude-code/settings
- cursor-agent: 
  - `cli-config.json`
  - 有全局和项目的
  - https://cursor.com/cn/docs/cli/reference/configuration

## 恢复对话

不同 cli 恢复对话的命令略有不同：

```sh
# claude 会自动保存对话，意外退出后，可以使用下面的命令，恢复对话，然后选择需要的上下文
claude --resume 

codex tbd

# gemini 不会自动保存会话，需要手动对话过程中，使用/chat 命令保存会话，意外退出，无法恢复
/chat list 列出保存的会话
/chat save <tag> 手动保存会话
/chat resume <tag> 恢复会话
/chat delete <tag> 删除会话
/chat share <tag> 使用md/json分享会话

gemini chat 的参考文档 https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/commands.md

qwen tbd
codebuddy tbd

# cursor-agent 自动保存会话，在合适的目录，运行下面的命令即可恢复
cursor-agent resume # 恢复最新对话
cursor-agent ls # 列出所有历史聊天记录
cursor-agent --resume="chat-id-here" # 恢复指定对话
参考文档: https://cursor.com/cn/docs/cli/overview#-3
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

cursor-agent # 在cursor IDE 安装，然后启动 cli 的时候，会弹出授权选项，通过即可
cursor IDE 一键安装 mcp 的网址  https://cursor.com/cn/docs/context/mcp/directory
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

### 文档
- [claude-code mcp](https://docs.claude.com/en/docs/claude-code/mcp)

## 高级技巧、案例

### 在 github action 中，使用 cursor-agent 做 code review
- 文档 https://cursor.com/cn/docs/cli/cookbook/code-review
- 这个文档有详细的工作流解释，推荐阅读

### 在 github action 中，使用 cursor-agent 自动检查 CI 失败的日志
- 文档 https://cursor.com/cn/docs/cli/cookbook/fix-ci
- 原理：
  - 检测CI运行失败，拉取代码库，安装 Cursor
  - 使用 cursor-agent -p <prompt> --force --model "$MODEL" --output-format=text
  - 在 <prompt> 使用 ${{ github.event.workflow_run.html_url }} 和 ${{ github.event.workflow_run.id }} 传入 github action 的运行记录，然后让 ai 使用  `gh run view` 等命令，抓取运行日志，然后修复，创建 PR

### 其他案例：
- github action 自动更新文档 https://cursor.com/cn/docs/cli/cookbook/update-docs
- github action 自动翻译i18n  https://cursor.com/cn/docs/cli/cookbook/translate-keys
- github action 自动密钥审计 https://cursor.com/cn/docs/cli/cookbook/secret-audit
- gitlab + claude 相关配置 https://docs.claude.com/en/docs/claude-code/gitlab-ci-cd

```shell
# 解读日志
tail -f app.log | claude -p "Slack me if you see any anomalies appear in this log stream"

# 分批提交代码
claude -p "Stage my changes and write a set of commits for them" \
  --allowedTools "Bash,Read" \
  --permission-mode acceptEdits
```

## 杂项
- iterm2 提示音
  - 任务在后台完成时，播放系统提示音
  - https://docs.claude.com/en/docs/claude-code/terminal-config#iterm-2-system-notifications
- VIM 模式
  - claude code /vim https://docs.claude.com/en/docs/claude-code/terminal-config#vim-mode
    - 模式切换
      - Esc：退回 NORMAL 模式。
      - i / I：在光标处插入 / 在行首插入。
      - a / A：在光标后插入 / 在行尾追加。
      - o / O：在下方新开一行 / 在上方新开一行并进入 INSERT。
  - 移动光标
      - h j k l：左、下、上、右。
      - w / e / b：下一个单词开头 / 当前或下一个单词结尾 / 上一个单词开头。
      - 0 / ^ / $：行首第 0 列 / 行首首个非空字符 / 行尾。
      - gg / G：跳到文件开头 / 文件结尾。
  - 编辑操作
      - x：删除光标下字符。
      - dw / de / db：删到下个单词开头 / 删到单词末尾 / 向后删一个单词。
      - dd / D：删除当前行 / 从光标删到行尾。
      - cw / ce / cb：改写到单词开头 / 单词结尾 / 向后一个单词。
      - cc / C：替换整行 / 从光标起替换到行尾。
      - .：重复上一次 Normal 模式命令，常用来快速连做相同操作。
  - cursor-agent /vim https://cursor.com/cn/docs/cli/reference/slash-commands

## 最后
这是 claude code 的官方文档，通读一遍，收获比刷x/短视频/公众号 要大很多： https://docs.claude.com/en/docs/claude-code/overview