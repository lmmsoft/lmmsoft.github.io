# Mingming's blog

Mingming's blog powered by Jekyll on Github, base on theme [Freshman21](http://github.com/yulijia/freshman21) Design by Lijia Yu, A tribute to WordPress Theme Twenty-Twelve and Twenty-eleven.

## 备注
1. 根目录里的x.md文件都会被渲染成首页的固定链接页面，用a_, b_, c_ .. 进行排序，是为了控制页面上的顺序，比如about想放第二个，就b_about

## Local Debug in Docker
总是 jekyll build 失败，记录下过程和相关资料，未来再说
- https://hub.docker.com/r/jekyll/jekyll/tags
- https://github.com/envygeeks/jekyll-docker/
- https://ddewaele.github.io/running-jekyll-in-docker/
- https://kuros.in/docker/docker-jekyll-container-to-serve-locally/ (dockerfile)

# github
- github的官方jekyll链接 https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/about-github-pages-and-jekyll

## 发布文章前的自查清单
- yml头里的日期是否正确？不能使用未来的时间，jekyll在编译时会忽略未来时间的文章
- 文件名是否符合规范？ 2023-03-01_xx_yy.md 就编译不出来，要用 2023-03-01-xx_yy.md 注意下划线
- 是否已使用 tekorrect -f _posts/2023-03-01-xx_yy.md 格式化文章?
- 是否需要加入 <!--more--> 标记，用于首页文章摘要显示
- 图片尺寸太大，是否需要压缩？ https://tinypng.com/ 调用api压缩，每个月免费500张，代码已实现

## Changelog
- 2023-03-30
    - 打通卡点，第一篇博客和公众号同发的文章
- 2023-03-22
  - 新增 Jekyll 的中文字数统计插件
  - 参考文章 https://blog.fooleap.org/jekyll-count-of-chinese-characters.html
  - 多语言没做，嫌麻烦，都是中文
- 2023-03-19
  - 使用chatgpt写代码，下载.md/.html文件中flickr的图片到本地，使用github做图床
- 2023-03-07
  - 安装 pangu 工具，用于中文排版自动格式化
> pip install -U pangu
> pangu -f ./_posts/2023-03-01-mac_finder_sort_photos_by_taken_time.md >> ./_posts/2023-03-01-mac_finder_sort_photos_by_taken_time.md
> tekorrect -f _posts/2023-03-01-mac_finder_sort_photos_by_taken_time.md
- 2023-03-02
  - 文章无法显示，经过检查，是文件名格式问题，错误❌2023-03-01_xx.md 正确✅2023-03-01-xx.md 太隐晦，太坑啦~
  - 图片可以使用 ![app](../images/xx.png) 格式, pycharm本地预览可以，github pages也可以正常显示
- 2023-02-21
  - about页 增加 访客地理位置统计地图 widget
    - https://clustrmaps.com/
    - 使用谷歌邮箱登录
- 2023-02-02
  - 增加 我的清单 页面
- 2023-02-01
  - 增加 plausible.io 统计，号称GA平替
- 2023-01-30
  - 全平台统一名称，博客从"明明如月的博客"改名为"明明如月成长笔记"
- 2023-01-30
  - 优化了友情链接，补充了推荐语description
- 2023-01-29
  - 根目录下非 _xxx 下划线开头的目录都会被发布到生成的网站中，输入 http://{site_url}/xxx/会自动打开xxx目录下的readme.md文件，所以把 xxx 改名成 _xxx 避免发布不必要的文件。 
- 2022-12-29
  - google analytics 更新，用 GA4 替换 UA，UA会在2023-06停止
  - 用 busuanzi 进行页面 PV/UV 统计
  - 用 jekyll-feed 生成 feed.atom, 同时也保留了 feed.xml(rss), 用 http://lmmsoft.github.io/ 网址订阅的话，默认用 atom 
- 2022-12-28
  - 重整 about 页面， 添加英文自我介绍，添加常用社交网站的链接
- 2022-12-27
  - 修复 category url 的bug, 因把页面permalink从 categories 改名成 category ，但超链接没更新导致
- 2022-12-05
  - 全站 https 
- 2021-11-25
  - 迁移博客园的文章

## 分类
2023-10-30 精简了分类之后，现有标签和文章数量，降序，供参考
- acm比赛 41 
- 我的游记 40
- 我的生活 39
- 挨踢生涯 33
- 我的思考 31
- 我的总结 20
- 有趣+好玩(博主推荐) 14
- 学习笔记 11 
- 我的练笔 9
- 我的影评 5
- 我的自由软件 3 
- 我的比赛 1
