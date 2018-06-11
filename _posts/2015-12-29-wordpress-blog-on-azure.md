---
title: My wordpress blog on Azure
date: 2015-12-29T17:32:26Z
author: lmm333
layout: post
permalink: /My-wordpress-blog-on-azure/
categories:
  - 修电脑
tags:
  - wordpress
  - azure
---

## 2015-12-30 Disable Plugin Replace-Google-Fonts

- Website very slow load, F12 tells me that [LINK](https://fonts.useso.com/css?family=Lato%3A300%2C400%2C700%2C900%2C300italic%2C400italic%2C700italic&amp;subset=latin%2Clatin-ext)  is time out
- [LINK](https://fonts.googleapis.com/css?family=Lato%3A300%2C400%2C700%2C900%2C300italic%2C400italic%2C700italic&amp;subset=latin%2Clatin-ext) is able to load under GFW
- So decative Plugin Replace-Google-Fonts

## 2015-12-30 Update DNS

- Move dns from the default sundns.com to dnspod.cn
- Step1. In sundns.com,  change dns address to f1g1ns1.dnspod.cn
- Step2: In dnspod.cn, add A name and C name
- Step3. In Azure manage page, get awverify url and set in dnspod.cn, such as awverify.www -&gt; cname-&gt; awverify.lmm333wiki.azurewebsites.net, Do this for both blog and wiki

## 2015-12-02 Add Archives page

- Install plugin [Archivist](https://wordpress.org/plugins/archivist-custom-archive-templates/)
- In plugin setting page, personalize archives page
- Add new page with [Archivist]

## 2015-04-30 Add view counts for each posts

- Install latest [wp-postviews](https://github.com/lesterchan/wp-postviews/) plugin(1.70)
- Edit Contest.php, add &lt;?php if(function_exists('the_views')) { the_views(); } ?&gt; after &lt;span class=&quot;comments-link&quot;&gt;

## 2015-02-07 Add Disqus

- Switch comments system form wumii to disqus, wumii support Chinese accounts logging such as QQ and weibo, but my posts hardly got comments within it. Since disqus is widely used in wp and gitbub blogs, I decide to try it, I didn't lose too much comments by this switch.

## 2015-01-31 Speed Up

-  Perf is terrible when loading, tried many ways, finally, the root casue is google font blocked by the 'wall'
1. Scale site to 2 cores, 3.5G
1. Set 'always on' on Azure site control pannel
1. Scale clearDB(MySQL) to improve sql performance(free plan is 20M in all , 13M now for blog+wiki )
1. F12 site loading processs, everything is ok(include site and flickr hosted photos), except 'fonts.googleapis.com/css?family=Lato' takes about 15 to load but still, it was blocked by the wall, my solution is to use  [http://libs.useso.com/ 360 cdn ] and  [http://www.amznz.com/fonts-googleapis-com-load-slow/ onts.googleapis.com加载慢解决办法 ] , install a plugin then active it

## 2014-09-26 Site Icon

- Add Meng favicon.ico to site(wiki and blog), so it has icon now
- Deploy the icon, FTP, one tricky is that the FTP address for the two sites(wiki and blog) is the same, user domain and pwd is different, my file explorer remember the user name and pwd of wiki, so I didn't update the blog successfully first(I thought it is blog at first,haha)

## 2014-04-09 Template

- update WP version to 3.8.2, according to the [introduction](http://blogs.msdn.com/b/azchina/archive/2014/03/03/wordpress-3-8-on-windows-azure-websites.aspx)
- change template to **twenty fourteen**
- deactive the plugin **MobilePress** as the wp 3.8 support mobile well and the views data and Google ads data could be well calculated on mobile now