---
layout: page
title: Travel
permalink: /travel/
toc: true
---

{% assign travel_year_count = site.data.travel | size %}
{% assign travel_trip_count = 0 %}
{% assign travel_spot_count = 0 %}
{% assign travel_post_count = 0 %}
{% for year_group in site.data.travel %}
  {% assign year_trip_count = year_group.trips | size %}
  {% assign travel_trip_count = travel_trip_count | plus: year_trip_count %}
  {% for trip in year_group.trips %}
    {% assign trip_spot_count = trip.spots | size %}
    {% assign travel_spot_count = travel_spot_count | plus: trip_spot_count %}
  {% endfor %}
{% endfor %}
{% for post in site.posts %}
  {% if post.travel_id %}
    {% assign travel_post_count = travel_post_count | plus: 1 %}
  {% endif %}
{% endfor %}

<div class="travel-page">
  <p class="travel-intro">世界很大，路要一步一步走。这里按时间记录我去过的城市、见过的风景，以及旅途中写下的文章。</p>

  <ul class="travel-stats" aria-label="旅行统计">
    <li><strong>{{ travel_year_count }}</strong><span>个年份</span></li>
    <li><strong>{{ travel_trip_count }}</strong><span>段行程</span></li>
    <li><strong>{{ travel_spot_count }}</strong><span>条地点记录</span></li>
    <li><strong>{{ travel_post_count }}</strong><span>篇相关文章</span></li>
  </ul>

  {% for year_group in site.data.travel %}
  <section class="travel-year" aria-labelledby="travel-{{ year_group.year }}">
    <h2 id="travel-{{ year_group.year }}">{{ year_group.year }}</h2>

    <div class="travel-list">
      {% for trip in year_group.trips %}
      <article class="travel-entry">
        <time class="travel-date">{{ trip.date }}</time>
        <div class="travel-main">
          <div class="travel-heading">
            {% if trip.title %}<span class="travel-title">【{{ trip.title }}】</span>{% endif %}
            {% unless trip.title == trip.place %}<span class="travel-place">{{ trip.place }}</span>{% endunless %}
          </div>
          <ul class="travel-spots" aria-label="地点和景点">
            {% for spot in trip.spots %}
            <li>{{ spot }}</li>
            {% endfor %}
          </ul>
        </div>

        {% assign related_posts = site.posts | where: "travel_id", trip.id | sort: "date" %}
        {% if related_posts.size > 0 %}
        <div class="travel-posts">
          <div class="travel-posts-label">相关文章：</div>
          <ul class="travel-posts-list">
            {% for post in related_posts %}
            <li><a href="{{ post.url | relative_url }}">{{ post.title }}</a></li>
            {% endfor %}
          </ul>
        </div>
        {% endif %}
      </article>
      {% endfor %}
    </div>
  </section>
  {% endfor %}
</div>
