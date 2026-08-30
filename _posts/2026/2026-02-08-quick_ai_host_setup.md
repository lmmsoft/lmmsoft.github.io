---
title:  "在AI时代，快速设置一台AI主机"
date: 2026-02-08T12:00:00+08:00
author: lmm333
layout: post
comments: true
published: true
permalink: /quick_ai_host_setup/
categories:
- 挨踢生涯
tags:
- AI
- 主机
- Linux
- NVIDIA
- CUDA
- Docker
- SSH
---

过去几年，“能跑得动模型”逐渐从极客玩具变成了日常生产力：写代码、做图、跑代理、做数据清洗、训练小模型、做 RAG……很多事情只要有一台稳定的 AI 主机，就能把「想法」直接变成「可复用的流水线」。

这篇文章记录一份我自己更偏向“少折腾、可复制、可长期维护”的快速搭建清单：从装系统到驱动、从容器到权限、从远程访问到监控与备份，目标是当天装好就能开始干活。
<!--more-->

## 0. 先说结论：我推荐的最小可用栈

- 系统：Ubuntu 22.04 LTS（或 24.04 LTS，但驱动/生态偶尔更挑）
- 驱动：NVIDIA 官方驱动（不要混装各种来源）
- 运行方式：Docker + `nvidia-container-toolkit`（尽量别让 Conda 把系统搞乱）
- 入口：SSH key + 非 root 用户 + 最少端口暴露
- 维护：日志、监控、磁盘/显存水位、定期备份

下面按我实际装机的顺序写。

## 1. 硬件与磁盘：别在“第一天”就把自己坑死

### GPU

- 推理为主：显存优先（24GB 起步更舒服）；多卡就看电源/机箱风道
- 训练/微调：显存 + 显存带宽 + NVLink（有则更好）；另外注意 CPU/内存别拖后腿

### 硬盘

- 系统盘与数据盘分离：系统盘 1TB 够用；数据盘按模型与数据规模来
- 文件系统建议：`ext4` 足够稳；要快照/压缩再考虑 `zfs/btrfs`

## 2. 安装 Ubuntu：一上来先把远程入口搞定

装完系统后第一件事：

1. 更新系统包
2. 创建非 root 用户并加进 `sudo`
3. 配 SSH key 登录，禁用密码登录（至少公网机器必须做）

示例（在主机上执行）：

```bash
sudo apt update && sudo apt -y upgrade
sudo adduser ai
sudo usermod -aG sudo ai
```

SSH 基础建议（`/etc/ssh/sshd_config`）：

- `PermitRootLogin no`
- `PasswordAuthentication no`
- `PubkeyAuthentication yes`

改完重启服务：

```bash
sudo systemctl restart ssh
```

如果要上公网，顺手把防火墙也开了（只放行你需要的端口）：

```bash
sudo ufw allow OpenSSH
sudo ufw enable
sudo ufw status
```

## 3. NVIDIA 驱动：只做一件事，做对

强烈建议通过 Ubuntu 推荐的方式安装驱动，并避免同时装 CUDA Toolkit、各种 runfile、以及第三方源造成的“混装”。

常用流程（选推荐版本）：

```bash
sudo ubuntu-drivers devices
sudo ubuntu-drivers autoinstall
reboot
```

重启后确认：

```bash
nvidia-smi
```

看到 GPU、驱动版本、显存信息正常，就先停在这里，别急着装一堆东西。

## 4. Docker + GPU：把环境封进容器，稳定性直接起飞

我倾向于把 “Python + CUDA + 各种依赖” 全都装进 Docker 容器，主机只负责：驱动、Docker、SSH、磁盘与监控。

### 安装 Docker

Ubuntu 上按官方方式装即可，装完确认：

```bash
docker --version
```

把你的用户加入 `docker` 组（避免每次 `sudo`）：

```bash
sudo usermod -aG docker $USER
newgrp docker
```

### 安装 nvidia-container-toolkit

装完后验证容器能看到 GPU：

```bash
docker run --rm --gpus all nvidia/cuda:12.4.1-base-ubuntu22.04 nvidia-smi
```

输出正常说明「驱动 + 容器」这条链路打通了，后面你用 PyTorch / vLLM / Ollama / ComfyUI 都会省很多心。

## 5. 一个“能直接用”的目录结构

我通常会这样放：

```text
/data
  /models        # 各种模型权重
  /datasets      # 数据集（如有）
  /work          # 你自己的项目/脚本
  /cache         # HuggingFace / pip 等缓存（可选）
```

然后用 Docker 把它们挂进去，容器里统一从 `/data` 访问，避免“跑着跑着找不到文件”的混乱。

## 6. 进阶但很值：监控、日志、备份

这部分决定了你的 AI 主机能不能长期稳定跑：

- 监控：至少要能看到 CPU/RAM/磁盘、GPU 利用率/显存/温度、网络
- 日志：服务类程序用 `systemd` 或容器日志集中管理，避免“出问题时没证据”
- 备份：代码与配置上 Git；数据盘定期做增量备份（至少有一份异地）

我自己的底线是：机器坏了/系统重装，1 小时内能把服务恢复到可用。

## 7. 经验教训：少踩坑的几条

- 先把驱动链路跑通（`nvidia-smi` + 容器 `nvidia-smi`），再开始装框架
- 不要在主机上把 Python 环境装成“史诗巨坑”，容器化能省大量维护时间
- 公网机器千万别裸奔：SSH key、禁 root、最少端口、最好再加 Fail2ban
- 给散热与稳定性留余量：显卡跑满时温度与功耗会“很真实”

---

如果你愿意，我可以下一步把这份清单升级成可直接复用的仓库结构：提供一个 `docker-compose.yml`，把常用的推理服务（比如 vLLM / Text Generation WebUI / Ollama / ComfyUI）一键拉起，并且把模型缓存、日志、反向代理、开机自启都安排好。
