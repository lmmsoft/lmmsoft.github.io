# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

这是一个基于Jekyll的个人博客，拥有19年的内容积累（2006-2025），托管在GitHub Pages上。博客包含437篇文章，涵盖ACM竞赛、旅行游记、IT职业生涯和个人思考。内容主要为中文，支持多语言界面。

## 开发命令

### 本地开发
- `_preview.sh` - 启动Jekyll开发服务器，支持草稿和未来文章（端口4000）
- `make serve` - 基于Docker的本地开发服务器，使用Jekyll 3.8.5（端口3000或4000）
- `make build` - 基于Docker的Jekyll构建，验证站点是否能正常编译

### 内容管理
- `_new_draft.sh [文件名]` - 从`_drafts/`中的模板创建新草稿
- `_publish.sh 文件名.md` - 将草稿移动到`_posts/`，自动添加日期前缀并处理git操作

### 内容质量工具
- `pangu -f 文件名.md` - 格式化中文排版和空格（自动在中英文之间添加空格）
- `tekorrect -f 文件名.md` - 应用文本校正（修复常见拼写和标点错误）
- 建议发布前总是运行这两个工具确保内容质量

## 架构说明

### 内容结构
- **`_posts/`** - 已发布的博客文章（437个文件，时间跨度2006-2025）
- **`_drafts/`** - 草稿文章，包含template.markdown新文章模板
- **`_layouts/`** - Jekyll模板文件（default, page, post）
- **`_includes/`** - 可复用组件（header, footer, sidebar, analytics）
- **`_sass/`** - SCSS样式表
- **`images/`** - 按文章日期和主题组织的图片
- **`_markdown-to-wechat/`** - 自定义微信发布工具

### 导航页面
根目录的markdown文件使用前缀控制菜单顺序：
- `a_home.md`, `b_about.md`, `c_archives.md`, `d_category.md`, `e_tags.md`, `f_guestbook.md`, `f_list.md`

## 发布流程

1. 创建草稿：`_new_draft.sh 文章标题`
2. 在`_drafts/`目录中编辑内容
3. 预览：`_preview.sh` 或 `make serve`
4. 格式化：对中文内容使用`pangu -f 文件名.md`和`tekorrect -f 文件名.md`
5. 验证：运行`make build`确保没有构建错误
6. 发布：`_publish.sh 文件名.md`（自动处理git add/mv操作）

## 重要注意事项

### 文件命名规范
- 文章必须使用格式：`YYYY-MM-DD-标题.md`（使用连字符，不是下划线）
- YAML头部的日期不能是未来时间（Jekyll会忽略未来的文章）

### 内容规范
- 添加`<!--more-->`标记用于首页摘要显示
- 优化大图片（可使用tinypng.com API集成）
- 中文内容应使用pangu/tekorrect工具格式化

### 多语言支持
网站通过`_config.yml`配置支持中文、英文、日文、波兰文、韩文、俄文、土耳其文和印尼文界面。

## 分析和集成
- Google Analytics 4
- 不蒜子页面访问统计
- Plausible.io替代分析
- Disqus评论系统
- jekyll-feed生成RSS/Atom订阅