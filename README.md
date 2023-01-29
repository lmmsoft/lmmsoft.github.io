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

## Changelog
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
- 2011-11-25
  - 迁移博客园的文章