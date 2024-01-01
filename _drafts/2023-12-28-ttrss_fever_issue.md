---
title:  "Welcome to Jekyll!"
date: 2023-12-28T00:00:00+08:00
author: lmm333
layout: post
comments: true
published: true
permalink: /ttrss_fever_issue/
categories:
- x
tags:
- a
- b
---

ttrss_fever_issue

    To login with the Fever API, set your server details in your favourite RSS application to: http://xxx.me:181/plugins.local/fever/

总是404

有两个插件目录， plugins 和 plugins.local, 各有一部分插件，fever在plugins里面

http://xxx.me:181/plugins/fever/ 就可以了！

```shell
/var/www/plugins # ls
af_comics             af_zz_vidmute         bookmarklets          hotkeys_noscroll      note                  toggle_sidebar
af_psql_trgm          auth_internal         cache_starred_images  hotkeys_swap_jk       nsfw
af_redditimgur        auth_remote           fever                 index.html            share
af_youtube_embed      auto_assign_labels    hotkeys_force_top     no_iframes            shorten_expanded
```

```shell
/var/www/plugins.local # ls
api_feedreader         feediron               mercury_fulltext       options_per_feed       wallabag_v2
api_newsplus           index.html             opencc                 remove_iframe_sandbox
```