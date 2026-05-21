---
title: "让 Codex App 和 CLI 单独走代理：不再和 VPN 抢系统代理"
date: 2026-05-21T00:00:00+08:00
author: lmm333
layout: post
comments: true
published: true
permalink: /codex-process-proxy/
categories:
- 挨踢生涯
tags:
- Codex
- AI
- 代理
- ClashX
- VPN
- CLI
---

## 一句话总结

如果你在香港或其他网络环境里使用 Codex 时需要代理，但工作内网、学校资源又经常需要 VPN，最省心的做法不是长期打开系统代理，而是只在启动 Codex App 或 Codex CLI 的那个进程里注入代理环境变量。这样代理默认可以关闭，VPN 也不用和全局代理互相打架。

<!--more-->

## 背景：系统代理和 VPN 很容易互相影响

我平时在香港使用 Codex，连接 GPT 服务通常需要走代理。但公司电脑还有另一个现实问题：工作时经常要拨内网 VPN，有时访问学校资源也要拨 VPN。

如果把系统代理长期打开，VPN、内网地址、学校资源和代理软件就容易互相影响。结果是：

- 浏览器或公司内网访问可能异常；
- 学校资源可能因为代理出口不对而打不开；
- Codex 又可能因为 VPN 改了路由，反而连不上模型服务；
- 每次都手动开关系统代理，很烦，也容易忘。

这几天我试了一种更简单的方式：系统代理保持关闭，只在启动 Codex App 或 Codex CLI 时，让这个进程和它的子进程带上代理配置。实测 Codex App 这条路径很有效；Codex CLI 这边我还会继续观察，但原理一致，可以先按同样方式配置。

## 先从 ClashX 复制终端代理命令

我用的是 ClashX。ClashX 菜单里有一个「复制终端代理命令」功能，复制出来大概是这一句：

```sh
export https_proxy=http://127.0.0.1:7890 http_proxy=http://127.0.0.1:7890 all_proxy=socks5://127.0.0.1:7890
```

这句话的意思是：只对当前终端会话设置代理。你可以先在一个终端窗口里执行它，然后测试命令行网络是否能走代理。

但我不建议把这句直接长期写成全局默认值。因为一旦写进 `~/.zshrc` 顶层，每个终端、每个 CLI、甚至一些开发工具都可能默认走代理，问题又回到原点。

更好的做法是：把代理设置包进函数里，只有运行这个函数时才生效。

## 方案一：只让 Codex App 走代理

把下面这段放到 `~/.zshrc`：

```sh
function Codex_APP() {
    (
        export http_proxy="http://127.0.0.1:7890"
        export https_proxy="http://127.0.0.1:7890"
        export HTTP_PROXY="$http_proxy"
        export HTTPS_PROXY="$https_proxy"
        export no_proxy="localhost,127.0.0.1,::1"
        export NO_PROXY="$no_proxy"

        # App 走 Chromium/Electron 的 --proxy-server 参数即可。
        # 避免把 SOCKS / npm / TLS 相关配置误带给其他子进程。
        unset all_proxy ALL_PROXY
        unset npm_config_proxy npm_config_https_proxy
        unset NODE_TLS_REJECT_UNAUTHORIZED

        mkdir -p "$HOME/Library/Logs/com.openai.codex"
        log="$HOME/Library/Logs/com.openai.codex/manual-launch-$(date +%Y%m%d-%H%M%S).log"

        "/Applications/Codex.app/Contents/MacOS/Codex" \
          --proxy-server="http://127.0.0.1:7890" \
          > "$log" 2>&1 &
    )
}
```

保存后执行：

```sh
source ~/.zshrc
Codex_APP
```

重点有三个：

1. 外层用了 `(...)` 子 shell，所以这些代理环境变量只在本次启动 Codex App 时生效，不会污染当前终端。
2. `--proxy-server="http://127.0.0.1:7890"` 会让 Codex App 这个 Electron/Chromium 进程走指定代理。
3. 日志会写到 `~/Library/Logs/com.openai.codex/`，如果 App 启动失败，可以先看最新的 `manual-launch-*.log`。

上面的路径默认假设 Codex App 安装在 `/Applications/Codex.app`。如果你和我一样没有装到 Applications 目录，比如放在 `~/code/Codex.app`，只需要改这一行：

```sh
"/Applications/Codex.app/Contents/MacOS/Codex" \
```

改成你的实际路径即可：

```sh
"$HOME/code/Codex.app/Contents/MacOS/Codex" \
```

## 方案二：只让 Codex CLI 走代理

Codex CLI 可以用同样思路处理。把下面这段也放到 `~/.zshrc`：

```sh
function Codex_CLI() {
    (
        export http_proxy="http://127.0.0.1:7890"
        export https_proxy="http://127.0.0.1:7890"
        export HTTP_PROXY="$http_proxy"
        export HTTPS_PROXY="$https_proxy"
        export all_proxy="socks5://127.0.0.1:7890"
        export ALL_PROXY="$all_proxy"
        export npm_config_proxy="$http_proxy"
        export npm_config_https_proxy="$https_proxy"
        export no_proxy="localhost,127.0.0.1,::1"
        export NO_PROXY="$no_proxy"

        codex --dangerously-bypass-approvals-and-sandbox "$@"
    )
}
```

之后启动 CLI：

```sh
source ~/.zshrc
Codex_CLI
```

如果你不想默认进入 `--dangerously-bypass-approvals-and-sandbox` 模式，也可以把最后一行改成更保守的：

```sh
codex "$@"
```

或者保留函数代理能力，把运行参数留给调用时决定：

```sh
Codex_CLI --dangerously-bypass-approvals-and-sandbox
```

## 不建议默认设置 NODE_TLS_REJECT_UNAUTHORIZED=0

有些代理环境里，为了绕过证书问题，会看到这句：

```sh
export NODE_TLS_REJECT_UNAUTHORIZED="0"
```

这会让 Node.js 跳过 TLS 证书校验。它确实可能临时绕过一些公司代理或中间人证书问题，但安全风险很高，不建议默认写进函数。

如果你的环境确实必须这样才能跑通，建议只在临时排障时加，并且明确知道自己在做什么。日常配置里，能不加就不加。

## 为什么这比开系统代理更稳

这套配置的核心是「进程级代理」：

- Codex App 通过环境变量和 `--proxy-server` 走代理；
- Codex CLI 通过环境变量走代理；
- 其他应用、浏览器、内网工具、学校 VPN 不受影响；
- 代理软件可以继续在本机监听 `127.0.0.1:7890`，但系统代理不需要长期打开。

这样做以后，日常使用路径会变成：

1. ClashX 保持运行，本地代理端口可用；
2. macOS 系统代理默认关闭；
3. 需要 Codex App 时运行 `Codex_APP`；
4. 需要 Codex CLI 时运行 `Codex_CLI`；
5. 工作 VPN、学校 VPN 按原来的方式拨号，不再因为全局代理互相干扰。

## 快速排查

如果配置后 Codex 仍然不能用，可以按下面顺序检查：

1. **确认 ClashX 本地端口。** 默认常见是 `127.0.0.1:7890`，但你自己的配置可能不同，以 ClashX 复制出来的终端代理命令为准。
2. **确认 App 路径。** 如果不是 `/Applications/Codex.app`，一定要改成实际路径。
3. **看启动日志。** Codex App 函数会把日志写到 `~/Library/Logs/com.openai.codex/`。
4. **确认函数是否生效。** 修改 `~/.zshrc` 后，要执行 `source ~/.zshrc`，或者新开一个终端窗口。
5. **不要同时开太多层代理。** 如果系统代理、VPN、ClashX TUN、终端代理同时开启，排查会变得很困难。建议先从「系统代理关闭 + 只用函数启动 Codex」开始。

## 小结

对我来说，这个方案解决的是一个很具体但高频的问题：Codex 需要代理，工作和学校资源又需要 VPN，系统级代理一开就容易互相影响。

把代理限制在 Codex App / CLI 启动进程里之后，默认网络环境保持干净，只有 Codex 自己走代理。需要时一条命令启动，不需要时完全不影响其他程序。

这类小配置不复杂，但能显著减少每天在代理、VPN、CLI 之间来回切换的摩擦。
