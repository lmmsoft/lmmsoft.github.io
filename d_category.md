---
layout: page
title: Categories
permalink: /category/
---

<ul class="tags-box">
{% if site.posts != empty %}
{% for cat in site.categories %}
    <a href="#{{ cat[0] }}" title="{{ cat[0] }}" rel="{{ cat[1].size }}">{{ cat[0] | join: "/"}}<span class="size"> {{ cat[1].size }}</span></a>
{% endfor %}
</ul>

<ul class="tags-box">
{% for cat in site.categories %}
    <li id="{{ cat[0] }}">{{ cat[0]}}</li>
    {% for post in cat[1] %}
        <time datetime="{{ post.date | date:"%Y-%m-%d" }}">{{ post.date | date:"%Y-%m-%d" }}</time> &raquo;
        <a href="{{ site.baseurl }}{{ post.url }}" title="{{ post.title }}">{{ post.title }}</a><br />
    {% endfor %}
{% endfor %}
{% else %}
<span>No posts</span>
{% endif %}
</ul>

