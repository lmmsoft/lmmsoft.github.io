---
title: My MediaWiki on Azure
date: 2015-12-02T10:11:16Z
author: lmm333
layout: post
permalink: /my-mediawiki-on-azure/
categories:
  - 挨踢生涯
tags:
  - azure
  - mediawiki
---

This is wiki about page, I will write down the edit log here.

## Upgrade Media from v1.20 to v1.26 (Fix no content error)

- BUG: No content in page, but has content in edit page:[bug detail](https://www.mediawiki.org/wiki/Thread:Project:Support_desk/Content_Not_Showing_In_Wiki/reply)  
- From this [Page](https://www.mediawiki.org/wiki/Manual:Errors_and_symptoms#All_pages_have_no_content.2C_but_when_editing_a_page_the_wiki_text_is_there) , I found it's unable to downgrade PCRE on Azure, the only way is to upgrade mediawiki
- Upgrate steps:
1. Add to Git by azure web page in case rollback needed
2. Clone to local, download v1.26 and merge files
3. Run update.php for datebase upgrade from azure debug console page: https://lmm333wiki.scm.azurewebsites.net/DebugConsole
4. cd to site\wwwroot, run "php maintenance/update.php "
5. Update LocalSetting.php file from the [Official Upgrate Guide](https://www.mediawiki.org/wiki/Manual_talk:Upgrading)
6. Open site [version page](http://wiki.lmm333.com/index.php?title=Special:Version) to check if all extension works well: 

## Add Google Analytic

- [Extension](http://www.mediawiki.org/wiki/Extension:Google_Analytics_Integration)

## 2015-01-31 Change Logo

- edit  $wgLogo to "favicon.ico" in LocalSettings.php in FTP folder
- http://www.dadclab.com/archives/1991.jiecao

## 2015-01-31 Add Mobile Support [Faled]

- Find mobile extension *MobileFrontend*   [Official site](http://www.mediawiki.org/wiki/Extension:MobileFrontend) , [Chinese Introduction](http://www.uedsc.com/mobilefrontend-mediawiki.html)
- MobileFronted need Mediawiki 1.24 at least, I am 1.20.3 now, Azure is 1.23 now
- "This version of MobileFrontend requires MediaWiki 1.24, you have 1.20.3. You can download a more appropriate version from https://www.mediawiki.org/wiki/Special:ExtensionDistributor/MobileFrontend"

## 2014-3-22 Add Markdown support

- find markdown extensions **MarkdownSyntax** in [official extension page](http://www.mediawiki.org/wiki/Extension_Matrix/beta)
- install the extension successfully with the [wiki page](http://www.mediawiki.org/wiki/Extension:MarkdownSyntax) and ftp login, remember the ftp user name is **domain\user**

## 2014-1-9

- find markdown extensions in [official extension page](http://www.mediawiki.org/wiki/Extension_Matrix/beta)
- install markdown extension [MarkdownExtraParser](http://www.mediawiki.org/wiki/Extension:MarkdownExtraParser) , but failed finally
  - note:
  - [AlternateSyntaxParser](http://www.mediawiki.org/wiki/Extension:AlternateSyntaxParser) only support v1.6 or above, it won't work on azure mediawiki now

## 2014-1-1 hello world

- hello world
- install mediawiki v1.2 in Azure
    - add domain **wiki.lmm333.com** in azure management panel
- edit LocalSettings.php in wwwroot folder
    - change **$wgServer** to "http://wiki.lmm333.com/";  ,so that links on wiki page will direct to **[wiki.lmm333.com](http://wiki.lmm333.com/)**, rather than azurewebsites.net

## automate generated

MediaWiki has been successfully installed

Consult the [//meta.wikimedia.org/wiki/Help:Contents User's Guide] for information on using the wiki software.

### Getting started ##

* [//www.mediawiki.org/wiki/Manual:Configuration_settings Configuration settings list]
* [//www.mediawiki.org/wiki/Manual:FAQ MediaWiki FAQ]
* [https://lists.wikimedia.org/mailman/listinfo/mediawiki-announce MediaWiki release mailing list]
