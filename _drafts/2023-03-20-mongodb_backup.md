---
title:  "mongodb自动备份与恢复"
date: 2023-03-20T00:00:00+08:00
author: lmm333
layout: post
comments: true
published: false
permalink: /mongodb_backup/
categories:
- 挨踢生涯
tags:
- mongodb
- 备份
---
这两天学习了 mongodb 的备份和恢复命令，可以使用容器里的 mongoexport/mongoimport/mongodump/mongorestore 命令来备份和恢复数据，并且做成了github action 的定时任务，每天把备份的数据提交的私有的代码仓库，这里记录一下。

## 备份命令
```shell
# mongoexport/mongoimport 是按照单表导入导出为 json/csv 的命令
mongoexport  --host HOST:PORT --authenticationDatabase admin -u USERNAME -p PASSWORD --db db_name --collection collection_name --out edx.json
mongoimport  --host HOST:PORT --authenticationDatabase admin -u USERNAME -p PASSWORD --db db_name --collection collection_name --file edx.json

# mongodump/mongorestore 可以按照整个数据库导入导出，也可以按照单表导入导出
mongodump    --host HOST:PORT --authenticationDatabase admin -u USERNAME -p PASSWORD --db db_name --collection collection_name --out edx-dump
mongorestore --host HOST:PORT --authenticationDatabase admin -u USERNAME -p PASSWORD --db db_name --collection collection_name --writeConcern="{w:0}" -edx-dump/edx/collection_name.bson

# 如果不传 --db db_name --collection collection_name 参数，会导出所有的数据库(db)里的所有表(collection)
mongodump    --host HOST:PORT --authenticationDatabase admin -u USERNAME -p PASSWORD --out .
# 恢复的时候，至少要制定 -db db_name 参数，不然会报错
mongorestore --host HOST:PORT --authenticationDatabase admin -u USERNAME -p PASSWORD --db db_name .

```
## 容器里备份
```shell
# 拉取容器镜像
docker pull mongo:4.4

# 后台启动容器，挂载本地目录（不挂载的话，文件会在容器里，备份后可以恢复，但是不方便提交到git代码仓库）
docker run --name mongo4 -d -v `pwd`:/backup mongo:4.4

# 备份容器内的数据库的所有表当前目录
docer exec -w /backup mongo4 mongodump  -u USERNAME -p PASSWORD --port 27017 --authenticationDatabase admin --out .
# 备份远程数据库的所有表当前目录
docer exec -w /backup mongo4 mongodump  --uri "mongodb://USERNAME:PASSWORD@domain.com:27017" --authenticationDatabase admin --out .

# 删除容器
docker rm -rf mongo4
```

## github action 里每天定时备份
```yaml
name: mongodb backup

```

- 试过 MongoDB in GitHub Actions， 好像没有 mongodump 命令
  - https://github.com/marketplace/actions/mongodb-in-github-actions
- 于是改用docker, github action 运行docker 参考这里
  - https://github.com/marketplace/actions/docker-run-action

## 踩坑
我使用了Azure Cosmos DB for MongoDB，底层是 Azure Cosmos DB， 上层给了MongoDB的API，所以可以使用MongoDB的命令来操作，但是有一些限制，比如不支持retryWrites，这里记录一下踩坑的过程。

1. 把本地数据恢复到 Azure Cosmos DB for MongoDB 遇到了 ```MongoError: Retryable writes are not supported. Please disable retryable writes by specifying "retrywrites=false" in the connection string or an equivalent driver specific config. ``` 问题，原因是Azure Cosmos 不支持 retrywrites ，[网上给的解决方案](https://stackoverflow.com/questions/68201298/cosmos-db-retryable-writes-are-not-supported-please-disable-retryable-writes-b)是连接字符串里加上 ```retryWrites=false```，但是我这里不行，Azure给的默认连接字符串里就有 ```retryWrites=false```， 最后经过尝试，把本地的 mongdb 容器从5.x降到4.x就可以了，参考命令```docker run --name mongo4 -d mongo:4.4```。
2. 把本地数据恢复到 Azure Cosmos DB for MongoDB 遇到了 ```limit-total-account-throughput```问题，这是因为免费的Azure Cosmos DB for MongoDB 有[1000 RU/秒的限制](https://learn.microsoft.com/zh-cn/azure/cosmos-db/limit-total-account-throughput)，我尝试了 ```mongorestore``` 命令后补充 ```--maintainInsertionOrder --numParallelCollections=1 --numInsertionWorkersPerCollection=1``` 参数，限制并发，但还是不够，于是在仪表盘里提高了总吞吐量的限制设置，可能在备份时会产生少许的费用。

## 参考文献
- Azure的mongo备份文档 https://learn.microsoft.com/zh-cn/azure/cosmos-db/mongodb/tutorial-mongotools-cosmos-db#choose-the-proper-mongodb-native-tool