---
title:  "仅让 Codex CLI / Codex App 走代理：进程级代理设置，避免与 VPN 冲突"
date: 2026-05-21T12:00:00+08:00
author: lmm333
layout: post
comments: true
published: true
permalink: /codex_proxy_per_process/
categories:
- 挨踢生涯
tags:
- Codex
- 代理
- VPN
- macOS
- ClashX
- CLI
---

## 背景：为什么要“只让 Codex 走代理”？

我在香港，Codex 连接 OpenAI 经常需要走代理；但日常工作还要连公司内网 VPN、学校资源 VPN。

如果把系统代理/终端代理长期打开，VPN 一拨就容易出现 **代理与 VPN 路由冲突**，导致 Codex 不可用（或者内网不可达）。

我的目标是：

- 代理默认保持关闭；
- 只有 **Codex App** 和 **Codex CLI** 这两个进程在启动时“临时带上代理环境”；
- 其它程序完全不受影响。

<!--more-->

这类做法本质上是 **进程级代理（per-process proxy）**：

- 不改系统网络代理
- 不污染当前终端的全局环境变量
- 只给某一个命令/应用的启动进程注入 `http_proxy/https_proxy/all_proxy` 等变量

下面以 macOS + ClashX 为例。

## 0. 先拿到 ClashX 的“终端代理命令”

ClashX 里有个常用功能：**复制终端代理命令**。

复制出来一般是这样的一行（你也可以先在终端临时执行它验证代理可用）：

```sh
export https_proxy=http://127.0.0.1:7890 http_proxy=http://127.0.0.1:7890 all_proxy=socks5://127.0.0.1:7890
```

这行命令里的 `127.0.0.1:7890` 取决于你 ClashX 的端口设置。

接下来我们不会把它“常驻”在环境里，而是封装成两个函数：`Codex_APP` / `Codex_CLI`，只有调用函数时才生效。

## 1. 写进 ~/.zshrc：Codex_APP（只让 Codex App 走代理）

把下面内容追加到 `~/.zshrc`：

```sh
# Codex_APP: 仅以“当前启动进程”的方式让 Codex App 走代理
function Codex_APP() {
  (
    # 1) 代理地址（按需改端口）
    local proxy_http="http://127.0.0.1:7890"

    export http_proxy="$proxy_http"
    export https_proxy="$proxy_http"
    export HTTP_PROXY="$http_proxy"
    export HTTPS_PROXY="$https_proxy"

    # 2) 建议保留本地直连
    export no_proxy="localhost,127.0.0.1,::1"
    export NO_PROXY="$no_proxy"

    # 3) 避免其它工具链变量干扰（按需精简/扩展）
    unset all_proxy ALL_PROXY
    unset npm_config_proxy npm_config_https_proxy
    unset NODE_TLS_REJECT_UNAUTHORIZED

    # 4) Codex App 的路径：默认按 /Applications 安装
    #    如果你装在别的目录：把这里改成你的实际路径即可
    local codex_bin="${CODEX_APP_BIN:-/Applications/Codex.app/Contents/MacOS/Codex}"

    # 5) 记录日志，方便排查是否真的带了代理启动
    local log_dir="$HOME/Library/Logs/com.openai.codex"
    mkdir -p "$log_dir"
    local log="$log_dir/manual-launch-$(date +%Y%m%d-%H%M%S).log"

    # 6) Electron/Chromium 系应用常见的代理参数：--proxy-server
    "$codex_bin" \
      --proxy-server="$proxy_http" \
      > "$log" 2>&1 &
  )
}
```

使用方式：

```sh
source ~/.zshrc
Codex_APP
```

如果你的 Codex.app 不在 `/Applications`，可以在 `~/.zshrc` 里加一行自定义路径（或直接修改函数里的路径）：

```sh
export CODEX_APP_BIN="$HOME/code/Codex.app/Contents/MacOS/Codex"
```

然后再执行 `Codex_APP` 即可。

## 2. 写进 ~/.zshrc：Codex_CLI（只让 Codex CLI 走代理）

Codex CLI 我这边还在继续验证最小环境变量集，但思路与 App 完全一致：只在子进程里 export 代理变量。

```sh
# Codex_CLI: 仅在执行 codex CLI 的这个进程里注入代理环境
function Codex_CLI() {
  (
    export http_proxy="http://127.0.0.1:7890"
    export https_proxy="http://127.0.0.1:7890"
    export HTTP_PROXY="$http_proxy"
    export HTTPS_PROXY="$https_proxy"

    export all_proxy="socks5://127.0.0.1:7890"
    export ALL_PROXY="$all_proxy"

    export no_proxy="localhost,127.0.0.1,::1"
    export NO_PROXY="$no_proxy"

    # 某些 Node 工具/包管理器会读这些变量；是否需要取决于你的网络环境
    export npm_config_proxy="$http_proxy"
    export npm_config_https_proxy="$https_proxy"

    # 如果你遇到企业证书/中间人导致的 TLS 报错，才考虑打开这个。
    # 安全性不佳：能不用就别用。
    # export NODE_TLS_REJECT_UNAUTHORIZED="0"

    # 你也可以按自己的习惯加 yolo 参数
    codex "$@"
  )
}
```

使用方式：

```sh
source ~/.zshrc
Codex_CLI --version
Codex_CLI --dangerously-bypass-approvals-and-sandbox
```

> 注：`--dangerously-bypass-approvals-and-sandbox` 是我个人习惯的“yolo 模式”。如果你更在意安全边界，可以不加。

## 3. 为什么这种方式能减少和 VPN 的冲突？

关键点有两个：

1. **代理变量只在子 shell 里生效**：
   - `(
       export ...
       codex ...
     )`
   - 子 shell 退出后，你当前终端的环境变量不会被污染。

2. **不改系统代理**：
   - 系统代理一旦打开，很多 GUI App/系统组件都会走代理；
   - VPN 重新下发路由/网关时更容易“你中有我，我中有你”。

而现在我们把“需要代理”压缩到最小范围：只给 Codex 进程。

## 4. 小坑与建议

- **no_proxy 一定要带 localhost**：否则很多本地服务（甚至你自己开的调试端口）会被错误地发到代理。
- **Codex App 的路径**：默认写 `/Applications/Codex.app/...`，但你装在其他目录就改 `CODEX_APP_BIN`。
- **NODE_TLS_REJECT_UNAUTHORIZED=0 慎用**：它会关闭 Node 的证书校验，能不用尽量不用。
- **排查**：App 启动后如果仍不通，先看 `~/Library/Logs/com.openai.codex/` 里的启动日志。

## 5. 总结

当你同时需要“代理访问 OpenAI”与“VPN 访问内网/学校资源”时，把代理做成 **进程级开关** 是非常顺手的工程化解法：

- 平时不影响任何其它程序
- 需要时一条命令启动 Codex App / Codex CLI
- 跟 VPN 的冲突面最小

后续我会继续补充：Codex CLI 在不同网络环境下最小变量集、以及更通用的“任意 App 进程级代理模板”。
