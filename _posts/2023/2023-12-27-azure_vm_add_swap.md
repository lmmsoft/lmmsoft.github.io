---
title:  "Azure 免费虚拟机增加 swap 空间提高性能"
date: 2023-12-27T12:00:00+08:00
author: lmm333
layout: post
comments: true
published: true
permalink: /azure_vm_add_swap/
categories:
- 挨踢生涯
tags:
- Azure
- VM
---

Azure 免费的虚拟机的配置是 1核1G， 默认的 swap 大小是0，内存只有 1G，实在不够用，app 会被 kill 掉。

因为是 ssd 盘，适当增加点 swap 空间，可以提高物理内存利用率，避免 app 被 kill 掉。性能上损失应该不大

我的 1G 内存的虚拟机，加了 2G swap，目前运行良好，直接在命令行下启动的 app 很久没有被 kill 掉了。

<!--more-->

如果在 Azure 上面的 Ubuntu VM 需要增加 swap 内存,可以按以下步骤操作:
1. 使用`sudo fallocate -l [大小]G /swapfile`命令创建一个指定大小的 swap 文件,例如创建2G的 swap 文件:

```bash
sudo fallocate -l 2G /swapfile
```
3. 使用 `sudo chmod 600 /swapfile` 设置交换文件权限。
3. 使用 `sudo mkswap /swapfile` 将文件设置为交换区域。
4. 使用 `sudo swapon /swapfile` 启用交换文件。
5. 在 `/etc/fstab` 中添加 `/swapfile none swap sw 0 0` 使交换文件在启动时自动加载。

增加 swap 的主要作用是当物理内存不足时,把一部分磁盘空间虚拟成内存使用,避免程序被 OS kill 掉。

**优点**是可以提高物理内存利用率, **劣势**是会降低系统性能，因为磁盘比内存慢很多。

一般来说,适当增加些 swap 有助于系统稳定运行,但不要配置过大的 swap 空间,否则会导致系统慢。

一般来说，swap 空间的大小应该至少等于物理内存的大小，以便在发生内存不足时，可以将整个内存转储到 swap 空间中。

建议配置与物理内存相近的 swap 空间,比如内存1G可以配置1G或2G的 swap。