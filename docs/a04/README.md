# A04 个人博客升级与兼容性收尾

> 状态：**draft / needs-review**；日期：2026-10-05。
> 范围：`lmmsoft/lmmsoft.github.io`；不部署正式站点。

## 1. 决策摘要

首选继续使用现有 **Jekyll 单体静态站**，先收敛构建版本、建立生成物兼容性门禁，并修复 RSS 2.0 的错误 self URL。Astro/EmDash 只保留为以后有数据证明收益时的备选，不在 A04 最小范围迁移。这样不引入第二套内容库、数据库、Serverless 或付费服务，也不把私人 KB 接入公开构建。

本薄切片包含：

1. Docker 使用 `BUNDLE_FROZEN=true` 防止构建时修改锁文件；构建由与 `Gemfile.lock` 冲突的 Jekyll 3.8.5，改为 Ruby 3.3.6 + Bundler 2.4.19，并由锁文件安装 Jekyll（当前锁定 4.4.1）。
2. PR 触发相同的生产构建与兼容性验证，但明确不部署；每个 PR 使用独立并发组，不会取消正式部署。
3. 标准库验证器检查旧入口、两个 feed、图片入口、旅行页相关文章链接及对应目标文件、Disqus 嵌入。错误 XML 会作为门禁失败报告。
4. 修复 `/feed.xml` 中指向不存在 `/zfeed.xml` 的 self link，并避免 `site.url` 尾斜杠导致双斜杠 URL。

回滚：整体可通过 `git revert <A04 commit>` 原子回滚；若只需撤销构建收敛，可恢复 `makefile` 与工作流；若只需撤销 RSS 行为，可单独恢复 `feed.xml`。本变更不改 permalink、内容数据或生产状态，无数据迁移/回填。

## 2. 来源与对账边界

需求来源为维护者提供的 A04 工作范围；本实现仅使用公开博客仓库中的代码与内容。

- 代码仓库本地提交 `3f33c33 ADD: travel page` 已包含旅行页、`_data/travel.yml` 和文章 `travel_id`，因此没有重写旅行功能或导入私人数据。
- 本地重新统计：454 个文章源文件、112 条公开行程、60 个含 `travel_id` 的文章文件。只确认仓库静态状态，没有宣称这些记录已实时或逐设备复核。
- 2026-10-04 初次云端检视未具备 GitHub 认证；PR #40 在线状态仍未核验。2026-10-05 在独立稀疏克隆中基于 `origin/master` 保存补丁，基线提交为 `442da39aed370a33585286233c56ec4343c89701`，未检出大型媒体，未修改现有工作副本。

## 3. PRD

### 3.1 目标用户与场景

| 用户 | 场景 | 期望结果 |
|---|---|---|
| 博客维护者 | 本地预览、依赖升级、发布前检查 | 一条可复制的 Docker 命令链生成与 CI 一致的站点 |
| 内容读者 | 打开收藏的旧文章、分类/标签、旅行页和图片 | 原 URL 与核心浏览路径继续工作 |
| RSS 阅读器用户 | 继续订阅 RSS 2.0 或 Atom | feed 是有效 XML，自描述 URL 正确，文章 URL 无异常双斜杠 |
| 评论用户 | 从文章页加载历史 Disqus 线程 | `disqus_shortname` 和文章 URL 语义不变 |
| 审阅者 | 在 PR 中判断升级是否破坏站点 | PR 自动构建并运行兼容性契约，不触发部署 |

### 3.2 输入、输出与状态约定

**输入**：Git 跟踪的 Markdown/HTML、Liquid/Sass、`_config.yml`、`_data/travel.yml`、`images/` 和 `attachments/`；依赖仅来自 `Gemfile.lock`。私人 KB、Cookie、凭据、真实设备数据不是输入。

**输出**：Jekyll 生成的 `_site/`，其中 HTML、CSS、图片和 `/feed.xml`、`/feed.atom` 均为静态文件；`_site/` 不提交。验证器退出码 `0` 表示契约通过，`1` 表示至少一个阻断错误。GitHub Actions 的 `build` 成功是可审阅状态，`deploy` 只允许非 PR 事件运行。

**重复执行语义**：构建与验证均为幂等操作；对相同 checkout 和锁文件重复执行会覆盖 `_site/`，不改内容源。Bundler 下载缓存可能影响耗时，不影响输出契约。

### 3.3 现有能力与实际缺口

| 已有能力 | 重新对账结果 | 缺口/风险 |
|---|---|---|
| Jekyll + GitHub Pages Actions | 工作流 Ruby 3.3、Bundler 2.4.19，锁文件 Jekyll 4.4.1 | `make build` 却固定 Jekyll 3.8.5，开发/CI 漂移 |
| 旅行页 | 112 行程、60 个带关联文章文件，Liquid 自动关联 | 历史准确性和真机移动端未实时复核；本期不改数据 |
| RSS + Atom | `/feed.xml` 手写 RSS，插件生成 `/feed.atom` | RSS self link 错指 `/zfeed.xml`；拼 URL 可能出现 `//` |
| 评论 | Disqus 静态嵌入 | 只能验证嵌入保留，云端不登录验证第三方线程 |
| 分类/标签/旧 URL | 既有 permalink 与静态入口 | 原工作流没有 PR 级生成物契约 |
| 图片 | 仓库约 1.3 GiB、2616 个文件 | 全量视觉和外链可用性成本高，本期只守固定图片入口 |
| 移动端样式 | Sass 已有 palm media query，旅行页已有响应式规则 | 无浏览器/设备实测记录；需预览后人工验收 |

### 3.4 最小范围与不做项

**最小范围**：统一构建入口；PR 构建；对关键输出做机器验证；修正 RSS 自描述链接；提供运行、验收、回滚文档。

**明确不做**：

- 不迁移 Astro、EmDash 或其他框架；不双写模板。
- 不更改文章 permalink、分类/标签命名、Disqus shortname 或旅行数据。
- 不导入或链接私人 KB，不发布未来行程、住宿、地址或交通班次。
- 不新增数据库、Serverless、定时器、付费 SaaS；不部署、不合并。
- 不把 mock 或源文件静态扫描冒充完整构建/设备验收。

### 3.5 首选与备选方案

**首选：原位收敛 Jekyll。** 保持当前内容模型与 Liquid，Ruby/Bundler 版本和 CI 对齐，通过小型 Python 标准库脚本定义迁移安全线。变更面最小，回滚简单，无新增运行成本。

**备选：并行生成器概念验证。** 只有当 Jekyll 构建时长、维护故障率或安全升级出现可量化且持续的问题时，才在临时分支以公开合成样例评估 Astro/EmDash。进入迁移前必须证明 URL 清单、两个 feed、图片路径、Disqus identifier、分类/标签、旅行关联与移动端差异全部可控；概念验证不得替换生产构建。

### 3.6 用户流程与运行位置

1. 维护者 checkout 分支，运行 `make build`；Docker 内安装锁定 Bundler 和锁文件依赖，生成 `_site/`，宿主 Python 验证契约。
2. 本地预览运行 `make serve` 后访问 `http://localhost:4000/`，检查桌面与 375px 手机视口：首页、文章、分类、标签、旅行页；停止容器即结束，不产生云服务。
3. 提交 PR 后，GitHub Actions 在 `ubuntu-22.04` 构建、验证、上传预览构建 artifact；PR 事件跳过 deploy。
4. 合并仍由维护者决定；A04 不执行合并或正式部署。

维护责任：仓库维护者维护 Gemfile/锁文件与内容；修改固定 URL、feed、评论或旅行模板的人同步更新验证器；GitHub 托管 runner 与 Pages 的可用性由 GitHub 提供，故障时不绕过门禁发布。

### 3.7 成本与未验证项

| 项目 | 固定成本 | 按量/电费 | 维护成本 | 状态 |
|---|---:|---:|---|---|
| 本地 Docker 构建 | 0 新增 | 使用开发机 CPU/网络/电费；数值未测 | 依赖升级时更新 lock | Docker 在本云端不可用，未实测耗时 |
| GitHub Actions/Pages | 0 新增服务 | 受仓库账户配额/政策影响 | 偶发 Action 升级 | 当前额度与未来政策未验证 |
| Python 验证器 | 0 | 可忽略 | 契约变更时更新 | 使用标准库 |
| Disqus/Analytics | 本期 0 新增 | 既有第三方策略决定 | 第三方脚本维护 | 线上加载、同意管理未实测 |
| Astro/EmDash | 本期 0 | 不适用 | 未采用 | 收益、迁移工时均未验证 |

### 3.8 失败恢复

- Bundler/网络失败：保留源文件不变，修复网络或使用已缓存依赖后原命令重跑；禁止用未锁定的全局 Jekyll 伪装通过。
- Jekyll 构建失败：停止，不生成可发布 artifact；依据首个错误修复并重跑。
- 兼容验证失败：CI 阻断；若是有意改变 URL，先提供重定向/订阅迁移方案并更新 PRD，再更新契约。
- 预览异常：不合并，截图记录视口与页面；可 `git revert` 回到旧构建/模板。
- Actions 故障：本地 `make build` 可复现，但不能替代合并前的 CI 记录。

### 3.9 分阶段任务

- **P0（本 PR）**：修复版本漂移与 RSS；增加 PR 构建和验证器；记录矩阵、验收与回滚。
- **P1（人工 review 后）**：在有 Docker 的机器跑 `make build`/`make serve`，保存桌面与手机截图；抽查历史 Disqus、RSS 阅读器、10 个旧 URL 与含图文章。
- **P2（可选）**：根据失败数据扩充 URL baseline 和图片引用检查；执行一次灾备回滚演练。
- **P3（条件触发）**：只有量化指标支持时才做候选框架 PoC 和迁移 ADR。

### 3.10 可复现验收标准

1. `make build` 在 Docker 可用且能访问 RubyGems 的环境退出 0，且实际使用锁文件；日志显示 Jekyll 4.4.1、Bundler 2.4.19。
2. `python3 scripts/verify_site.py _site` 退出 0；固定入口、RSS/Atom XML、RSS self link、旅行文章链接、Disqus 嵌入均通过。
3. PR 工作流 build 通过且 deploy 显示 skipped；push 到允许分支时原部署拓扑不变。
4. `make serve` 后桌面与 375×812 视口无横向溢出；导航中“我的清单”在“旅行”之前；旅行关联可点击。
5. 抽样旧文章 URL、分类、标签、图片均返回 200；RSS 阅读器可重新拉取且无需改订阅 URL。

## 4. 需要用户决定（不阻塞薄切片）

1. **是否把 GitHub Pages 的实际发布源固定为 Actions？** 当前仓库已有部署工作流，但未在本环境读取仓库 Settings；review 后确认即可。
2. **是否接受 Jekyll 4.4.1 为基线，还是将 Gemfile 收紧为 `~> 4.4.1`？** 本 PR 保持现有约束与 lock，避免额外依赖变更。
3. **P1 的移动端验收设备**：优先指定 Chrome 375×812 + 一台真实 iOS/Android；若只做浏览器仿真，需要明确接受第三方评论的设备差异风险。
