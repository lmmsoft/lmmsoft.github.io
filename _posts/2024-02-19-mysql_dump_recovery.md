---
layout: post
title: "用 Docker 恢复 phpMyAdmin 里的 MySQL 备份"
date: 2024-02-19 22:00:00 +0800
author: lmm333
comments: true
permalink: /mysql_dump_recovery/
categories:
  - 挨踢生涯
tags:
  - MySQL
  - phpMyAdmin
  - Docker
---

备份数据库的时候只需要点几下导出，真正用得上备份的时候往往才是麻烦的开始。最近在本地调试一个旧项目时，需要把早前通过 phpMyAdmin 导出的 SQL 文件还原回来，于是顺手记录一下整个过程以及踩过的坑。

<!--more-->

## 准备镜像和数据卷

我选择直接用官方的 `mysql:8` 镜像配合一个临时的数据卷。这样既不会污染主机环境，也方便反复尝试。大致的初始化命令是：

```bash
docker volume create mysql-data

docker run \
  --name mysql-recovery \
  -e MYSQL_ROOT_PASSWORD=example \
  -e MYSQL_DATABASE=legacy_app \
  -p 3306:3306 \
  -v mysql-data:/var/lib/mysql \
  -d mysql:8
```

等容器启动完成后，就可以用 phpMyAdmin 或者命令行客户端连接到 `localhost:3306`，验证数据库和用户是否创建成功。

## 导入 phpMyAdmin 导出的 SQL

phpMyAdmin 的导出文件本质上就是 `mysqldump` 的结果，因此可以直接使用 `mysql` 命令导入：

```bash
docker exec -i mysql-recovery \
  mysql -uroot -pexample legacy_app < backup.sql
```

需要注意的是，如果数据库已经存在同名表，导入会提示错误。可以提前在 SQL 文件里添加 `DROP TABLE IF EXISTS`，或者导入前通过 phpMyAdmin 删除旧表，避免重复。

## 常见问题与解决

- **连接中断**：第一次导入时因为网络不稳导致 SSH 会话断开，命令半途而废。后来改用 `screen`/`tmux` 或者直接在容器里执行脚本，就可以不中断地完成导入。
- **安全警告**：终端会提示 `mysql: [Warning] Using a password on the command line interface can be insecure.`。这只是提醒密码暴露在命令行参数中，临时环境可以忽略，生产环境建议改用环境变量或 `.my.cnf`。
- **字符集乱码**：如果 SQL 文件里没有显式指定字符集，可以在导入命令前加上 `SET NAMES utf8mb4;`，或者在 phpMyAdmin 导出时勾选 `Add SET NAMES` 选项。

## 小结

整个流程其实并不复杂：准备好隔离的容器环境，把 SQL 文件挂进去执行导入命令，遇到报错逐条分析即可。写下来之后，下次再遇到类似的恢复需求，直接照着步骤操作就能快速复现环境。
