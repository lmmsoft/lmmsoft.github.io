# A04 兼容性矩阵

> 状态：**draft / needs-review**。矩阵区分“源代码确认”“生成物自动验证”和“待人工/线上验证”，避免把 mock 当真实验收。

| 能力 | 当前契约 | 自动检查 | 本次差异 | 状态 / 后续 |
|---|---|---|---|---|
| 默认分支 | GitHub 公共页面显示 `master` | 无 | 不改 | 2026-10-04 页面确认；Settings 未读取 |
| 生产构建 | Ruby 3.3 + Bundler 2.4.19 + lock 中 Jekyll 4.4.1 | CI `bundle exec jekyll build` | Make 从 Jekyll 3.8.5 对齐此链路 | 云端缺 Docker/RubyGems 403，待 CI 实证 |
| 首页与旧 URL | permalink 不变 | `/index.html` 和固定入口存在 | 不改 permalink | URL 全量 baseline 为 P1/P2 |
| RSS 2.0 | `/feed.xml` | XML 可解析，self URL 精确匹配 | `/zfeed.xml` 修为 `/feed.xml`；使用 `absolute_url` | 源码已测；需真实构建 |
| Atom | `/feed.atom` | XML 可解析 | 不改 | 真实阅读器待测 |
| 图片 | 原 `/images/**` 路径 | `/images/favicon.ico` 存在 | 不搬迁/压缩 | 全量引用/浏览器加载待测 |
| 评论 | Disqus shortname `lmm333` | 至少一页含 embed | 不改 identifier/shortname | 历史线程与第三方加载待线上人工测 |
| 分类 | `/category/` | 固定入口存在 | 不改 | 内容抽样待测 |
| 标签 | `/tags/` | 固定入口存在 | 不改 | 内容抽样待测 |
| 旅行页 | `/travel/`；YAML + Liquid + `travel_id` | 相关文章列表非空且站内链接目标存在 | 不改 112/60 数据 | 桌面/手机和历史准确性待人工复核 |
| 导航 | 清单后为旅行 | 构建间接覆盖 | 不改 | 源码确认；浏览器待测 |
| 移动端 | 既有 Sass palm breakpoint | 暂无视觉自动化 | 不改样式 | 375×812 截图待有浏览器环境执行 |
| CI/部署 | push 构建并部署 | PR 构建/验证，deploy skipped，并发组独立 | 新增 PR 门禁 | 不部署；需 PR run 实证 |
| 回滚 | Git revert | 无破坏性数据操作 | 单提交可逆 | merge 前可直接关闭 PR |

## 验证差异记录（2026-10-04）

- **已执行并通过**：Python 脚本语法编译；对合成静态站 fixture 的成功与故障路径测试；工作树 diff/空白检查。
- **已执行但受限**：`bundle check` 明确显示依赖未安装；`bundle install` 因 RubyGems 网络返回 403 失败；环境没有 Docker，不能在此云端生成 `_site`。
- **未冒充完成**：生产构建、Jekyll doctor、桌面/手机浏览器截图、线上旧 URL/第三方评论、PR #40 在线状态。
- **数据对账**：当前仓库重新统计为 454 个文章源文件、112 条旅行记录、60 个带 `travel_id` 的文章；数量不是内容真实性验收。

## 合成 fixture 约定

验证器测试只能创建临时目录，放置最小 HTML/XML/空图片；不得复制私人 KB 或真实凭据。fixture 用于验证检查器自身的 pass/fail 语义，不等价于 Jekyll 构建通过。

## 2026-10-05 独立克隆复核

- `python3 -m unittest discover -s tests -p 'test_verify_site.py' -v`：5/5 通过（正常站点、RSS self URL 错误、无效 XML、导航冒充相关文章、文章目标缺失）。
- `make -n build serve` 与 `git diff --check`：退出 0；只说明命令展开和补丁格式有效。
- Docker 已在沙箱外只读复核：daemon 未运行；本机 Ruby 2.6 没有锁定的 Bundler 2.4.19。未启动或安装运行时，完整生产构建与 `jekyll doctor` 仍未执行。
- 稀疏克隆未检出图片和附件；合并前的完整 checkout/CI 必须执行真实构建与兼容性门禁。
- 修复 PR 并发取消正式部署的风险；移除公开文档里的私人聊天链接和私人来源路径；未改生产数据。
