---
title:  "Fix Synology Web Clipper Login Issue 修复群晖笔记剪藏插件登陆问题"
date: 2023-01-11T20:00:00+08:00
author: lmm333
layout: post
comments: true
published: true
permalink: /fix_synology_web_clipper_login_issue/
categories:
- 修电脑
tags:
- 群晖
- Synology
---

### English Version:

I met login issue when Synology Web Clipper plugin(for DS Note) was auto upgraded to lastert version(v3.0.116) by Chrome browser on Dec 2022.

Many users met the same issue and comment on chrome webstore, but no official reply yet.

I think it was because of the newest v3 release, so I tried to delete latest v3 version and install an old v2 version, it works~!

You can download v2.0.111 crx file which was released on June 2022 by this [link](https://www.crx4chrome.com/go.php?p=305957&i=pcfbfimijgibligmbglggnbiobgjgmbk&s=zs9xSBGT8DO2s&l=https%3A%2F%2Ff6.crx4chrome.com%2Fcrx.php%3Fi%3Dpcfbfimijgibligmbglggnbiobgjgmbk%26v%3D2.0.111), or find more versions from this [page](https://www.crx4chrome.com/history/10755/).

Have a good day~!

### 中文版：

最近(2022年12月)群晖DS Note的网页剪藏插件Synology Web Clipper不能登陆，及时之前处于登陆状态的也无法剪藏，完全无法使用。
<!--more-->
我去看了chrome应用商店，很多人都在反馈这样的问题，有中文、英文、俄文等各种语言，看来不是我一个人的问题。

评论里没找到解决方案，我尝试自己解决，经过调查，感觉2022年12月30日发布的v3.0.116嫌疑最大！

搜索历史记录，发现之前2022-12-25发布过v3.0.115，而再上一个版本是2022-06-13发布的v2.0.111。

从v2跨越到v3，估计有很大的升级，错误大概率出现在这里！

猜想12-25号发布的版本，可能有Bug，于是在12-30发布了修复，没完全修好，但是程序员休新年假期去了，而谷歌浏览器的插件有自动更新功能，导致大量用户受到影响。

于是我尝试回滚到旧版本v2.0.111，成功登陆！

可以使用[这个链接](https://www.crx4chrome.com/go.php?p=305957&i=pcfbfimijgibligmbglggnbiobgjgmbk&s=zs9xSBGT8DO2s&l=https%3A%2F%2Ff6.crx4chrome.com%2Fcrx.php%3Fi%3Dpcfbfimijgibligmbglggnbiobgjgmbk%26v%3D2.0.111)下载v2.0.111，先在设置里删除最新版本的插件，再把下载好的crx文件拖入浏览器安装，亲测有效！

如果你想尝试其他旧版本，也可以在[这里](https://www.crx4chrome.com/history/10755/)搜寻。

希望本文能解决你的问题^^ 如果有效，欢迎在下面评论或点赞，谢谢！

### My comments on Chrome App Store:

If you meet login issue after 2022-12, you can try to downgrade to previous version. Please refer my post for solution and download link: https://lmmsoft.github.io/fix_synology_web_clipper_login_issue/
如果你遇到登陆在2022年底之后遇到了登陆问题，大概率是新版本差点，可以看看我的解决方案: https://lmmsoft.github.io/fix_synology_web_clipper_login_issue/

