---
title: "把两台 Kindle Paperwhite 2 变成冰箱家庭信息面板"
date: 2026-07-27T00:00:00+08:00
author: lmm333
layout: post
comments: true
published: true
permalink: /kindle-fridge-dashboard/
categories:
  - 挨踢生涯
tags:
  - Kindle
  - 电子墨水屏
  - Python
  - 家庭自动化
  - SSH
---

家里有两台已经吃灰的 Kindle Paperwhite 2。它们的电池依然能用，电子墨水屏也很适合长期显示静态内容，于是我把它们改造成了两块冰箱家庭信息面板：天气、家庭待办、生日倒计时和每日一首古诗都放在一页里。

<!--more-->

这不是在 Kindle 上跑一个网页。真正的做法是：家里的 Mac 动态生成一张严格符合 Kindle 分辨率的灰度 PNG，Kindle 按计划通过 HTTP 下载，再由屏保插件把它刷到电子墨水屏上。

## 最终效果

两台设备共用同一套后端，但各自有独立页面。第一台显示「珊瑚海兔生日」，第二台显示「虹虹生日」。

![第一台 Kindle 的真实 framebuffer 截图](/images/2026/2026-07-27-kindle-fridge-dashboard/lmm333-kindle-framebuffer.png)

![第二台 Kindle 的真实 framebuffer 截图](/images/2026/2026-07-27-kindle-fridge-dashboard/fion-kindle-framebuffer.png)

这两张图不是浏览器预览，也不是服务器原图，而是通过 Kindle 自带的 `/usr/sbin/screenshot` 从设备 framebuffer 直接取回的截图。它们可以确认软件实际显示的内容和裁切情况；坏点、残影、屏裂等物理问题仍要以肉眼为准。

## 整体架构

数据流很简单：

```text
香港天文台 API + 本地家庭配置
              │
              ▼
家中 Mac：Python + Pillow 动态渲染
              │
              ├── /dashboard.png
              └── /dashboard_fion.png
                         │
                         ▼
Kindle：onlinescreensaverPW2 定时 wget
                         │
                         ▼
linkss 屏保目录 → eips 刷新电子墨水屏
```

正常刷新只走 HTTP，不依赖 SSH。SSH 是独立的维护通道，用于安装、排障、取 framebuffer 截图和更新 Kindle 端脚本。

Mac 上的服务由 LaunchAgent 托管，监听家庭局域网端口。两个 URL 对应两个配置文件，所以两台 Kindle 可以复用天气、待办和古诗逻辑，又保留各自的生日倒计时。

## 硬件和软件

这次用到的主要组件：

- 两台 Kindle Paperwhite 2，固件均为 5.12.2.2；
- Kindle 越狱、KUAL 和 MRPI；
- USBNetwork：提供 SSH、SCP 和 SFTP；
- linkss：接管自定义屏保图片；
- 固定到特定 commit 的 `FalconFour/onlinescreensaverPW2`；
- 家中 Intel Mac 上的 Python、Pillow 和 LaunchAgent；
- 香港天文台开放数据 API。

服务端完整代码放在：

<https://github.com/lmmsoft/vibe/tree/main/02-project/kindle-fridge-dashboard>

## 第一步：先把内容压进 758×1024

PW2 的屏幕是 758×1024。电子墨水屏的限制反而让设计目标很清楚：

- 输出必须是 8-bit 灰度 PNG；
- 文字层级要足够明显；
- 避免大面积深色背景；
- 每个区块都要在一次全屏刷新里看清；
- 网络失败时保留上一张成功图片。

页面最终分成四块：

1. 香港天气；
2. 家庭待办；
3. 周年生日倒计时；
4. 每日古诗。

顶部显示日期、时间、最后更新时间和 Kindle 电量。

生日配置支持 `annual: true`。日期已经过去时，程序会自动计算下一年的同一天，而不是把倒计时显示成负数。古诗则按本地日期稳定轮换，同一天内多次刷新不会乱跳。

## 第二步：彩色 Emoji 必须重新画

最初我直接在待办里放了猪、书本、珊瑚、兔子、彩虹、蛋糕等 Emoji。结果 macOS 的字体渲染和彩色 Emoji 到 PW2 灰度屏后并不可靠：有的变成空框，有的丢失，还有的顺序错乱。

最后的处理方式是：

1. 从文字中解析已知 Emoji token；
2. 保留原始顺序；
3. 用 Pillow 的线条、圆弧、矩形和椭圆画成单色小图标；
4. 再把图标放到对应待办或倒计时右侧。

这比寻找「刚好能在所有环境中工作的 Emoji 字体」稳定得多，也更符合电子墨水屏的气质。

## 第三步：一套服务支持两台 Kindle

默认设备读取：

```text
config/dashboard.json
```

第二台访问 `/dashboard_fion.png` 时，服务自动读取同目录的：

```text
config/dashboard.fion.json
```

profile 名只允许小写字母、数字、下划线和连字符，避免路径穿越。配置在每次请求时重新加载，因此改待办、倒计时或古诗不需要重启服务；只有 Python 代码变化才需要重启 LaunchAgent。

两台设备在 Mac 的 SSH 配置里也使用独立别名和独立密钥：

```text
lmm333_kindle
fion_kindle
```

这样不会因为 IP 变化或多设备 host key 混用而连错机器。

## 第四步：Kindle 端的安装顺序

实际安装顺序是：

1. 确认越狱、KUAL、MRPI 正常；
2. 安装 USBNetwork；
3. 安装 linkss；
4. 为每台设备写入独立 SSH 公钥；
5. 先执行一次手动图片更新；
6. 检查屏幕和日志；
7. 最后才启用自动刷新。

项目里把容易出错的步骤做成了脚本。例如部署第一台：

```bash
./scripts/deploy-kindle-extension.sh \
  --host lmm333_kindle \
  --image-uri http://MAC_LAN_IP:42137/dashboard.png \
  --keep-wifi-on
```

第二台改用自己的别名和 profile URL：

```bash
./scripts/deploy-kindle-extension.sh \
  --host fion_kindle \
  --image-uri http://MAC_LAN_IP:42137/dashboard_fion.png \
  --keep-wifi-on
```

部署脚本会固定上游 commit、先上传到临时目录、原子替换扩展，然后执行一次手动更新。只有手动更新成功并确认屏幕正常后，才加 `--enable` 打开自动刷新。

## 第五步：USBNetwork 菜单最容易看反

USBNetwork 的 KUAL 菜单显示的是「点下去会执行什么」，不是「当前是什么状态」。

例如：

- 看到 `Disable SSH at boot`，反而表示当前已经启用开机 SSH；
- 看到 `Block SSH over WiFi`，表示当前 Wi-Fi SSH 已经开放；
- 看到 `Enable SSH over USB`，表示当前仍在 USBMS，SSH 只走 Wi-Fi；
- 看到 `SSHD: Use DropBear`，表示当前正在使用 OpenSSH。

我的目标模式是：

- Wi-Fi 上运行 SSH；
- USB 线仍保持普通存储盘；
- OpenSSH；
- 开机自动启动 SSHD；
- 每台设备保留独立密钥；
- 不做路由器公网端口映射。

项目默认只允许专用密钥。为了兼容旧设备上的应急维护，配置脚本也提供一个必须
显式开启的密码备用选项；如果使用它，至少要保留空密码和
keyboard-interactive 禁用，并为设备设置独立强密码。无论哪种方式，都不应该把
Kindle 的 root SSH 映射到公网。

如果只追求续航，可以让刷新脚本每次下载完图片后关闭 Wi-Fi。若要把 Kindle 当成长期可维护的家庭终端，则要接受 Wi-Fi 常开带来的额外耗电。

这里还有一个容易漏掉的细节：`wirelessEnable=1` 只代表系统设置里打开了 Wi-Fi。PW2 进入深度休眠后仍会给无线电断电，SSHD 虽然还在，网络却不可达。

真正的无人值守模式需要在屏保状态周期续期 `deferSuspend`，让设备停留在「Ready to suspend」而不进入深睡。原本依赖 RTC 唤醒的刷新，也要改成同一进程里的对齐计时器。这样才能同时得到：

- 屏保正常显示；
- Wi-Fi 和 SSH 持续可达；
- 15/60/120 分钟刷新继续执行。

代价也很直接：CPU 和 Wi-Fi 长期在线，耗电显著高于默认的 RTC 深睡模式。项目保留了两种部署方式，必须由使用者明确选择。

## 第六步：低功耗刷新和失败回退

当前计划：

- 00:00–06:00：每 120 分钟；
- 06:00–23:00：每 15 分钟；
- 23:00–24:00：每 60 分钟。

进入屏保和从休眠唤醒时也会触发更新。每次更新采用临时文件下载，成功后才替换正式屏保；服务器不可用、Wi-Fi 断开或图片下载失败时，不会覆盖上一张成功图片。

这一点很重要：冰箱上的信息面板宁可暂时旧一点，也不能变成白屏。

## 两个真实踩坑

### 1. 临时防休眠会让电源键看起来失效

部署时为了避免 Kindle 中途休眠，我临时设置过：

```text
preventScreenSaver=1
```

如果部署完成后忘记恢复，短按电源就不会进入屏保，看起来像电源键坏了。恢复为 `0` 后马上正常。后来我把「部署结束必须验证 `prevent_screen_saver:0`」加入了检查项。

### 2. `No` 也可能被当成真

Kindle 上的 `powerd_test` 返回：

```text
Charging: No
```

旧代码只排除了 `false`、`0` 和 `not charging`，于是字符串 `No` 被误判为正在充电。这个问题不是普通服务器预览发现的，而是在抓取第二台真实 framebuffer 截图时看到的。

修复后，充电状态只接受明确的真值：`1`、`true`、`yes`、`charging` 和 `on`，并补了单元测试。

## 验证清单

服务端：

```bash
uv lock --check
uvx ruff check .
uv run python -m unittest discover -s tests -v
curl -fsS http://127.0.0.1:42137/healthz
```

设备端：

```bash
./scripts/verify-kindle.sh --host lmm333_kindle
./scripts/verify-kindle.sh --host fion_kindle
```

另外还会核对：

- 设备序列号与 SSH 别名一致；
- 输出为 758×1024、8-bit 灰度 PNG；
- 自动刷新进程正在运行；
- 图片 URL 与设备 profile 一致；
- 重启后 SSHD 和自动刷新能自行恢复；
- 用另一台 Kindle 的密钥无法登录；
- 屏保状态保持 `preventScreenSaver=0`，同时出现 `defer_suspend:1`；
- 连续超过默认深睡窗口后，Wi-Fi 和 SSH 仍然可达；
- framebuffer 截图与预期内容一致。

## 小结

这个项目最有意思的地方，不是把网页截图塞进 Kindle，而是把一块十多年前的电子墨水屏重新变成家里每天都会看的东西。

Mac 负责数据、排版和动态生成，Kindle 只负责可靠地下载和显示；两者之间是最普通的 HTTP。系统足够简单，所以网络断了还有上一张图，服务重启了配置仍在，两台设备也可以继续增加自己的 profile。

旧硬件不一定要追求运行更多软件。让它只做好一件低功耗、可见、长期有用的事，反而更适合它。
