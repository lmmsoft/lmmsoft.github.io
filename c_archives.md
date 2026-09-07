---
layout: page
title: Archives
permalink: /archives/
---

<ul class="tags-box">

{% if site.posts != empty %}

{% for post in site.posts %}
{% capture this_year %}{{ post.qzone_display_date | default: post.date | date: "%Y" }}{% endcapture %}
{% unless year == this_year %}
{% assign year = this_year %}
{% unless post == site.posts.first %}
{% endunless %}
<li id="{{ year }}">{{ year }}</li>
{% endunless %}
<time datetime="{{ post.qzone_display_date | default: post.date | date:'%Y-%m-%d' }}">
{{ post.qzone_display_date | default: post.date | date:"%Y-%m-%d" }}
</time>
&raquo; <a href="{{ site.baseurl }}{{ post.url }}">{{ post.title | capitalize }}</a><br />
{% endfor %}

{% else %}

<span>No posts</span>

{% endif %}

</ul>
