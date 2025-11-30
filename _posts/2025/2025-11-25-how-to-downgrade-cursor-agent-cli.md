---
title:  "如何降级 cursor-agent /cursor-cli"
date: 2025-11-25T12:00:00+08:00
author: lmm333
layout: post
comments: true
published: true
permalink: /cursor_agent_downgrade/
categories:
- 挨踢生涯
tags:
- Cursor
- CLI
- AI
---

## 背景

遇到了新版 cursor-agent(2025.11.06-8fe8a63) 的奇怪 bug：光标总是自动滑到最后一行，导致输入混乱，而且长任务还会卡住。论坛已有反馈：<https://forum.cursor.com/t/cursor-cli-input-field-throws-cursor-at-end-of-line-at-every-character-and-freeze-on-long-running-script-task/142385>。

光标总是自动滑到最后一行这个不能忍，为了恢复可用，只能先降级。折腾了很久，总结出了几条可行路径，分享给同样被坑的老铁们。

<!--more-->

## 0. 官方安装脚本到底干了什么？

日常安装命令是：

```sh
curl https://cursor.com/install -fsS | bash
```

把脚本拉下来可以看到，里面写死了一个版本号，例如：

```
TEMP_EXTRACT_DIR="$HOME/.local/share/cursor-agent/versions/.tmp-2025.10.28-0a91dc2-$(date +%s)"
DOWNLOAD_URL="https://downloads.cursor.com/lab/2025.10.28-0a91dc2/${OS}/${ARCH}/agent-cli-package.tar.gz"
FINAL_DIR="$HOME/.local/share/cursor-agent/versions/2025.10.28-0a91dc2"
ln -s ~/.local/share/cursor-agent/versions/2025.10.28-0a91dc2/cursor-agent ~/.local/bin/cursor-agent
```

核心信息：

- 二进制下载地址格式：`https://downloads.cursor.com/lab/<版本号>/<OS>/<ARCH>/agent-cli-package.tar.gz`
- 安装后存放目录：`~/.local/share/cursor-agent/versions/<版本号>/`
- `~/.local/bin/cursor-agent` 只是指向该版本的 symlink

降级的本质就是：换用旧版本号、重新解压，并把 symlink 指向旧版本。

## 1️⃣ 方案一：本地已有旧版本时最简单

如果之前装过旧版，它很可能还在本地：

```sh
ls ~/.local/share/cursor-agent/versions
```

若能看到类似：

```
2025.08.15-dbc8d73
2025.09.18-7ae6800
2025.10.20-f1b214f
2025.10.22-f894c20
2025.10.28-0a91dc2
2025.11.06-8fe8a63
```

直接把 symlink 指回旧版本即可：

```sh
rm ~/.local/bin/cursor-agent
ln -s ~/.local/share/cursor-agent/versions/2025.10.28-0a91dc2/cursor-agent ~/.local/bin/cursor-agent
cursor-agent --version
```

这是最干净、最不折腾的方式。

## 2️⃣ 方案二：手工下载旧版本并“仿造安装”

### 2.1 一些已知可用的旧版本号

社区帖子里还能找到不少历史版本，例如：

- 2025.10.20-f1b214f
- 2025.10.22-f894c20
- 2025.10.28-0a91dc2

下载 URL 模板：

```
https://downloads.cursor.com/lab/<版本号>/<OS>/<ARCH>/agent-cli-package.tar.gz
```

`<OS>` 取 `linux` 或 `darwin`，`<ARCH>` 取 `x64` 或 `arm64`。例如下载 `2025.09.18-7ae6800` 的 macOS ARM64 包：

```sh
curl -fSL "https://downloads.cursor.com/lab/2025.10.28-0a91dc2/darwin/arm64/agent-cli-package.tar.gz" -o /tmp/cursor-agent.tar.gz
```

> 提醒：部分很旧或特殊 hash 的版本可能已被下架，可能直接 403 / AccessDenied。

### 2.2 手动“仿造安装流程”

下载成功后，可以用下列精简版安装脚本（支持自定义版本号）：

```sh
VER="2025.10.28-0a91dc2"
OS="darwin"   # 或 linux
ARCH="arm64"  # 或 x64

mkdir -p "$HOME/.local/share/cursor-agent/versions"
TEMP_EXTRACT_DIR="$HOME/.local/share/cursor-agent/versions/.tmp-$VER-$(date +%s)"

mkdir -p "$TEMP_EXTRACT_DIR"
curl -fSL "https://downloads.cursor.com/lab/$VER/$OS/$ARCH/agent-cli-package.tar.gz" \
  | tar --strip-components=1 -xzf - -C "$TEMP_EXTRACT_DIR"

FINAL_DIR="$HOME/.local/share/cursor-agent/versions/$VER"
rm -rf "$FINAL_DIR"
mv "$TEMP_EXTRACT_DIR" "$FINAL_DIR"

mkdir -p "$HOME/.local/bin"
rm -f "$HOME/.local/bin/cursor-agent"
ln -s "$FINAL_DIR/cursor-agent" "$HOME/.local/bin/cursor-agent"

cursor-agent --version
```

这基本就是官方脚本的精简可配版。

## 3️⃣ 方案三：保存官方脚本到本地，改版本号再执行

如果不想手写命令，可以把官方脚本下载到本地、替换版本号后执行：

```sh
curl https://cursor.com/install -fsS -o cursor-install.sh
```

把脚本里所有的 `2025.11.06-8fe8a63` 改成想降级到的版本号，例如 `2025.10.28-0a91dc2`，然后：

```sh
chmod +x cursor-install.sh
./cursor-install.sh
```

脚本会自动完成 OS/ARCH 检测与 PATH 提示，但若该版本的 tar.gz 被官方下架，依旧会下载失败。更换版本时也需要重新编辑脚本。

## 自动更新如何避免？

降级后，cursor-agent 仍可能后台自动下载新版，创建新的 `versions/<新版本>/` 目录并重写 `~/.local/bin/cursor-agent`。可以通过额外 alias 固定旧版本，例如：

```sh
alias cu2="$HOME/.local/share/cursor-agent/versions/2025.10.28-0a91dc2/cursor-agent --force"
echo "alias cu2=\"$HOME/.local/share/cursor-agent/versions/2025.10.28-0a91dc2/cursor-agent --force\"" >> ~/.zshrc
source ~/.zshrc

cu2 --version
```

- `cu` 继续跟随官方的自动更新（或你手动更新的 symlink）
- `cu2` 永远指向指定旧版本，互不冲突

这样即使自动更新覆盖了默认 symlink，也可以用 `cu2` 启动稳定的旧版继续干活。

## 后续

这个 bug 后续有很多人在论坛了讨论，过了几周官方才确认，又过了几个版本，在11月底的版本(2025.11.25-e276529)，终于修复了。

