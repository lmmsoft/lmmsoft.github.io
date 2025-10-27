---
title:  "在 MacOS 上，成功恢复存储卡上被误删的照片"
date: 2025-10-27T00:00:00+08:00
author: lmm333
layout: post
comments: true
published: true
permalink: /mac_file_recovery/
categories:
- 挨踢生涯
tags:
- MacOS
- 恢复
---
## 一句话总结
在 MacOS 电脑上，成功使用 PhotoRec 工具，恢复了存储卡上被误删的照片。

<!--more-->

## 意外的格式化事故

前几天宝宝在玩相机菜单时，不小心把相机的存储卡给格式化掉了。那张卡里保存着许多还没来得及备份的照片，结果全部被清空。

发现问题后，我立刻把存储卡拔出，防止继续拍照覆盖旧文件，这样才有机会恢复出被删除的照片。那是一张普通的 TF 卡，插回电脑后果然没有任何照片，只剩下一些相机自动生成的初始化文件。

## 搜索恢复方案

我用的是 macOS，于是开始在网上搜索“Mac 如何恢复格式化的存储卡”。网上广告和软文多得惊人，大多数都是需要付费的软件。试了几个之后都不太满意。最终，我找到了一个免费的老牌工具——PhotoRec。它是开源项目 TestDisk 套件的一部分，不收费用，只是建议用户捐赠支持。

## 免费但强大的 PhotoRec

PhotoRec 是一个命令行界面的恢复工具，和另一款带 GUI 界面的软件 Disk Drill 属于同源系列。相比之下，Disk Drill 对新手更友好，但免费版只能恢复 500 MB 数据，还有限制文件类型；PhotoRec 虽然界面朴素，但功能完整、真正免费。对熟悉命令行的用户来说，效率极高。

## 在 macOS 上的安装与启动

下载 PhotoRec 后，得到一个压缩包，解压后里面是若干命令行程序。第一次双击启动时，macOS 出现安全提示，阻止了运行。这时需要打开系统设置 → 隐私与安全性，手动允许该程序运行。

第二次启动时，程序提示要用 root 权限运行，否则可能无法访问物理磁盘。于是我打开 Terminal，在终端输入：

```shell
sudo <拖入程序路径>
```

按回车后输入密码，授予权限，系统还会弹窗请求访问“所有文件”等。确认后，就能看到熟悉的黑底命令行界面了。

## 实际恢复过程

PhotoRec 的操作逻辑并不复杂。

选择磁盘：它会列出所有可用磁盘和分区，包括硬盘、U 盘、存储卡等。我选中了那张 TF 卡。

选择文件系统格式：程序询问存储卡的格式，我的卡是 FAT32，因此选择了 “FAT/Other”。

选择输出目录：非常重要的一步，不要把恢复文件保存回原卡，否则会覆盖原数据。我在电脑主目录下新建了一个文件夹作为输出路径。

设置完毕后，程序开始逐扇区扫描。它没有太多花哨的可视化进度条，但效率很高。大约十几分钟后，扫描完成，输出目录里多出了几百张照片、视频以及一些零散文件。

## 对比其他工具

在使用 PhotoRec 之前，我也尝试过 Disk Drill。虽然它的界面更友好，但免费版只能预览，恢复需要付费几十美金。我最终放弃了 Disk Drill，转而使用 PhotoRec，全程零费用且恢复效果几乎一样。

## 使用感受与总结

PhotoRec 适合稍有电脑经验的用户使用。它没有图形界面，但命令行逻辑清晰、恢复效果扎实，不依赖网络，也不会强制收费。整个过程虽然略显“极客”，但我成功地把宝宝误删的照片全部救回来了。

写下这篇小记，一来是记录这次小危机的解决过程，二来也推荐这个实用又良心的工具——当你以为一切都没救时，PhotoRec 也许能帮你找回那些珍贵的记忆。

## 参考链接

[群晖的图文教程：如何使用PhotoRec恢复从Synology NAS意外删除的文件？](https://kb.synology.cn/zh-cn/DSM/tutorial/How_can_I_use_PhotoRec_to_recover_files_accidentally_deleted_from_my_Synology_NAS)

[PhotoRec 中文主页+下载地址](https://www.cgsecurity.org/wiki/PhotoRec_CN)

[PhotoRec 英文主页](https://www.cgsecurity.org/wiki/photoRec)

[github testdisk 开源地址](https://github.com/cgsecurity/testdisk)
