---
layout: page
title: Qzone 日志
permalink: /qzone/
---

这里收录从 QQ 空间迁移的日志。文章按原始发表日期排列，每篇保留来源记录；转载文章保留原文中的作者和来源说明。文中的想法、称呼和叙述属于当时的语境。

{% assign qzone_posts = site.tags.qzone | sort: "qzone_published_at" | reverse %}
{% assign qzone_years = qzone_posts | group_by_exp: "post", "post.qzone_published_at | date: '%Y'" %}

<p>共 <strong>{{ qzone_posts | size }}</strong> 篇日志。也可以通过 <a href="{{ '/tags/' | relative_url }}#qzone">qzone 标签</a>查阅。</p>

{% if qzone_posts != empty %}
<nav aria-label="按年份查看 Qzone 日志">
  {% for year in qzone_years %}
  <a href="#qzone-{{ year.name }}">{{ year.name }} 年（{{ year.items | size }}）</a>{% unless forloop.last %} · {% endunless %}
  {% endfor %}
</nav>

{% for year in qzone_years %}
<section aria-labelledby="qzone-{{ year.name }}">
  <h2 id="qzone-{{ year.name }}">{{ year.name }} 年</h2>
  <ul>
    {% for post in year.items %}
    <li><time datetime="{{ post.qzone_published_at | date: '%Y-%m-%d' }}">{{ post.qzone_published_at | date: '%Y-%m-%d' }}</time> — <a href="{{ post.url | relative_url }}">{{ post.title | escape }}</a></li>
    {% endfor %}
  </ul>
</section>
{% endfor %}
{% else %}
<p>暂时没有已迁移的日志。</p>
{% endif %}
