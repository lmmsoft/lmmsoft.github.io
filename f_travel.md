---
layout: page
title: Travel
permalink: /travel/
toc: true
---

<div class="travel-page">
  <p class="travel-intro">世界很大，路要一步一步走。这里按时间记录我去过的城市、见过的风景，以及旅途中写下的文章。</p>

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

        {% assign related_posts = site.posts | where: "travel_id", trip.id %}
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
