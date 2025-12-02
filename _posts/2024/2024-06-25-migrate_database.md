---
title:  "教育优惠到期，无法白嫖，我是如何迁移数据库的"
date: 2024-06-25T12:00:00+08:00
author: lmm333
layout: post
comments: true
published: true
permalink: /migrate_database/
categories:
- 挨踢生涯
tags:
- Azure
- MySQL
- PostgresSQL
---

![img_ttrss.png](/images/2024/2024-06-25-migrate_database/img_ttrss.png)

分享一下这几天迁移 selfhost 的 one-api/TinyTinyRSS 等服务和数据库的经历。

之前我通过在读的远程硕士学位，一直白嫖着微软Azure的教育服务，他们家的虚拟机、数据库、AI服务用着那叫一个爽。可谁能想到，今年白嫖失败啦，续期总是不成功，这一下子费用高得吓人，一个月账单要好几百呢！尤其是之前免费的 30G 可突发的 MySQL 和 postgres 数据库实例，每个月都得 $20 外加备份的存储费用，两个加起来就得四百多人民币，出账时真实肉痛啊！
<!--more-->
为了省钱，必须得迁移。考察了几种方案后，最后选择用 Docker 在虚拟机上搭建服务，这样虽然便宜不少，但在备份、安全、易用性等方面确实差了不少。毕竟之前我还遭遇过 [我也被黑客勒索攻击了](https://lmmsoft.github.io/hacked_for_ransom/)，就是搭建在 docker 里的 MariaDB，所以在这方面可得特别小心。

## MySQL 数据迁移

需要迁移的 MySQL 里有 one-api 和 trojan-web 的服务数据，PostgresSQL 里是 TinyTinyRSS 的数据。

trojan-web 的数据比较简单，数据库里的数据就几行，也不重要，我直接按照官方教程，先搭建 MariaDB，再重装服务。

one-api 里有我所有的 LLM 的 api-key，调用记录等，数据是有价值的，需要迁移。另外服务在线上使用，最好能有热迁移的方法。
![img.png](/images/2024/2024-06-25-migrate_database/img_1panel.png)
于是我先在 VM里，用 1panel 面板搭建了新 MySQL 服务(注意不用默认端口，降低在公网上被扫描攻击的可能)，然后在面板上备份了旧 MySQL 的对应库，生成了 xxx.sql.gz 的备份文件，再导入到新库，然后创建了一个新的 one-api 服务，使用不同的端口，确认服务正常。

此时无服务中断的迁移方法应该是把调用先迁移到新服务，再下线旧服务。我找了夜里没用调用量的时候，直接停止旧服务，改数据库连接，再启动，完成了迁移。相当于新服务只用于验证方案可行，然后旧服务做停机切换了。

完成 MySQL 迁移后，删除 Azure 上相关实例，开始省钱啦。

## PostgresSQL 数据迁移

原本想用同样的方法迁移 ttrss 在 PostgresSQL 里的数据，结果数据 2G 太大了，重复上面的步骤遇到问题。

于是搭建了 新的 PG 数据库和 pgadmin 服务, pgadmin 类似于 MySQL 的 phpmyadmin, 是个管理 pg 的 web 客户端。

在 B 站上现学了 pgadmin 的用法，然后在 UI 上点点鼠标，就好啦。

![img.png](/images/2024/2024-06-25-migrate_database/img_pgadmin.png)

迁移 ttrss 服务和数据库步骤是：
1. 先在 Server 上右键 Register 新旧两个数据库的连接，需要输入 域名/IP地址、端口、用户名、密码等信息。
2. 备份：在旧数据库的 ttrss 库上点击 Backup 按钮，备份，生成备份文件，我输入了文件名 backup-ttrss-2024-06，此时 Process 栏目下会有任务状态，取决于数据量和网速，我的2分钟就好了。
3. 恢复：在新数据库创建 ttrss 库，然后在新库上点击 Restore 按钮，选择刚才的备份文件，恢复。此时 Process 能看到任务状态，我这里也是5分钟就好了，虽然显示失败，但从日志上看到，是 azure 的管理用户恢复失败（因为我的库没有 azure 的特殊用户），不影响，相关数据的表对比了一下行数，都是正确的。
4. 在新机器上用 docker-compose.yml 配置，创建了新的 ttrss 服务，服务启动。此时数据库连同整个机器都卡了一小时左右，查了下监控，是 IO 打满了，我怀疑是因为数据量大，索引更新等原因导致的，等一会儿就好了。

完成迁移后，ttrss 的启动和运行速度都快了很多，可能是因为 ttrss服务和pg数据库放在了同一台机器上。 之前的服务是 pg 和 ttrss 分开的，pg 在 日本的 Azure 上，ttrss 在自家nas上，可能是网络延迟，导致网页打开速度太慢，难以忍受。

## 总结
虽然迁移的过程有点波折，但能解决问题还是很开心的！希望我的经历能给大家带来一些启发和帮助！
