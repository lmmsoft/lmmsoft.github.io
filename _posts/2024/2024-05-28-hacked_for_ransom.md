---
title:  "我也被黑客勒索攻击了"
date: 2024-05-28T12:00:00+08:00
author: lmm333
layout: post
comments: true
published: true
permalink: /hacked_for_ransom/
categories:
- 挨踢生涯
tags:
- 黑客
- 数据库
---
![hacked.png](/images/2024/2024-05-28-hacked_for_ransom/hacked.png)

## 一句话总结
经常在网上看到黑客勒索攻击的案例，没想到今天我也中招了！
<!--more-->

## 事情经过

早上起来，宝妈发现我搭建的开源工具不能使用，影响她科研，让我赶紧修复。

我试了一下，果然不能用，先登录了远程的虚拟机，发现机器服务正常。

继续登录管理网页，发现登不上去了，密码不可能被改，应该是数据库的问题。

![log.png](/images/2024/2024-05-28-hacked_for_ransom/log.png)

查看数据库容器的日志，发现了大量的 `[Warning] Access denied for user 'Test'@'94.232.45.152' (using password: YES) `， ip 地址各不相同，但都是一秒一次，很集中，我试着查了几个ip的来源，包括丹麦的🇩🇰荷兰🇳🇱白俄罗斯🇧🇾等地，应该是有黑客在爆破。

用 DataGrip 连 mariadb， 可以连上，但是 数据表没了，难道数据库损毁了么？

刷新连接，发现多了一个库，叫做 README_TO_RECOVER_TNA 感觉不妙！

里面有一个表，叫做 README，打开有一行数据(已隐藏黑客的具体信息)：

![db.png](/images/2024/2024-05-28-hacked_for_ransom/db.png)

```
I have backed up all your databases. To recover them you must pay 0.007 BTC (Bitcoin) to this address: xxx . Backup List: XXX. After your payment email me at xxx@airmail.cc with your server IP (20.x.x.x) and transaction ID and you will get a download link to your backup. Emails without transaction ID and server IP will be ignored. 
```

黑客的意思是备份了我数据，付他 0.007 个比特币，并发送相关信息到他的邮箱，他会给我备份的下载链接。

按照今天的 6.8wu 的价格，大约 476u, 约 3500 元。

## 对策和复盘：
1. 要不要付钱？不要，付了钱不保证有下载地址，有可能再被骗一次
2. 有没有备份？没有
3. 损失大不大？不大，只有少量开源软件的使用数据，不算太重要，重建服务也可以接受
4. 为什么会被攻击？ 主要原因是在搭建服务时，用了**开源项目教程里的默认密码**，其实一开始用了自定义的密码，但是遇到了连接问题，后来直接用默认密码就通了，就没进一步折腾了
5. 庆幸：因为云厂商的数据库比较贵，最近有计划把数据都迁移到这个虚拟机容器里的自建数据库。幸亏自己有点懒，拖着一直没有迁移，否则损失惨重。
   云厂商贵是有贵的道理的，点点鼠标就能带来的安全性+备份，自建省钱，但需要花很多时间学习和折腾，哪怕有AI帮助，学习的时间减少，折腾的时间也少不了！
6. 下一步：个人还有一些其他的数据库，裸奔的也不在少数。加备份，改密码，改端口，要提高安全级别呀！

如果你是我，你该怎么办？有更好的方法么，欢迎留言交流~
