---
layout: post
title: "Wordpress修改固定链接，配好重定向，依然404的解决方法"
date: 2016-06-30 23:52:58 +0800
comments: true
categories: 挨踢生涯
keywords: 404 cache wordprss link
permalink: /wordpress-404-redirct-cache-plugin/
---

今晚被坑了好久，最后发现是缓存问题，好好记录下过程：

因为博客搬家的缘故，搞重定向前想把链接改美好一点，于是在Wordpress管理界面里修改固定链接，从 domain/title/ 改成 domain/year/month/day/title，改完居然不奏效，记得以前是可以的，为什们呢？

网络搜索一番，都是说没配重定向，可是我有啊，而且正确，我用的是SAE， 服务器是nginx， 不能改.htaccess，二是通过SAE自己的AppConfig，修改目录下的config.yaml文佳，改成

``` plain
---
name: lmm333
version: 1
handle:
- rewrite: if (!is_file() && !is_dir() && path ~ "^/(.*)") goto "index.php/$1"
```

我的是对的，和网上的解决方案一模一样，改好之后首页的链接都自动变成了新的有年月日格式，但点击还是404，手打没年月日的网页就可以，然后就陷入很久的百思不得其解当中。

一会儿，有个思路是查查是不是有缓存：

1. 修改网站的配置文件，让网站强制刷新，不起作用

2. 查看wordpress是不是装了缓存插件比如wordpress-cache什么的，详细过了一遍开启的插件列表，没有

3. 突然发现插件列表最上面有个“Drop-in高级插件”的东西从来没见过，点开，果然是一个叫做object-cache.php的文件，好像是SAE memcache的插件，于是去了wp-content目录，强制删除了这个文件，药到病除~！
