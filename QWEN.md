# Mingming's Blog (lmmsoft.github.io)

## Project Overview

This is a Jekyll-powered GitHub Pages blog called "明明如月成长笔记" (Mingming's Growth Notes) by lmm333. The blog is built using the Freshman21 theme and hosted at https://lmmsoft.github.io/. It contains articles dating back to 2006, covering diverse topics such as ACM competitions, travel experiences, life reflections, technical notes, and personal growth. The content is primarily in Chinese, with some English content.

The blog features extensive personal content including life experiences, technical articles, travel journals, and thoughts on various topics. It covers:
- ACM competitions (41 articles)
- Travel experiences (40 articles)
- Personal life (39 articles)
- Professional development in DevOps, CICD, and engineering efficiency
- Sports and fitness (particularly triathlon, running, and swimming)
- Technical tutorials and development notes

## Project Structure

- `_posts/` - Contains dated blog posts following the format `YYYY-MM-DD-title.md`
- `_drafts/` - Draft posts that are not yet published
- `_includes/`, `_layouts/`, `_sass/` - Theme templates and styling
- `css/main.scss` - Main CSS file
- `images/` - Image assets
- `attachments/` - Additional file attachments
- Root-level markdown files (a_home.md, b_about.md, etc.) - Static pages with prefixed naming for ordering

## Building and Running

### Local Development
1. Install dependencies: `bundle install`
2. Build the site: `bundle exec jekyll build`
3. Serve with live preview: `bundle exec jekyll serve --host 0.0.0.0 --port 4000 --drafts --future --watch`
   - Or use the script: `_preview.sh`
4. Use `jekyll doctor` to check for configuration issues

### Docker-based Development
- Build: `make build` or `docker run jekyll/jekyll:3.8.5 build`
- Serve: `make serve` or `docker run -p 4000:4000 jekyll/jekyll:3.8.5 serve --host 0.0.0.0 --port 4000 --drafts --watch`

### Publishing Workflow
- Create drafts using `_new_draft.sh`
- Preview drafts with `_preview.sh`
- Publish to posts with `_publish.sh` (moves draft to `_posts/` with correct date prefix)

## Development Conventions

### Post Naming
- Posts must follow the format `YYYY-MM-DD-title-with-dashes.md`
- No underscores in the slug part of the filename
- Dates cannot be in the future (Jekyll ignores future-dated posts)

### Content Structure
- Each post must include YAML front matter with layout, title, date, categories, and tags
- Use `<!--more-->` to specify excerpt break point
- Apply Chinese typography formatting with `pangu` tool before publishing

### Code Style
- Sass files use four-space indentation
- YAML front matter uses two-space indentation
- Markdown content with semantic headings and fenced code blocks

### Commit Guidelines
- Use prefixes like `ADD:`, `FIX:`, `CHORE:` in commit messages
- Keep commits focused on a single concern
- Include generated assets when necessary

## Key Features

- Multi-language support (Chinese as default, with English, Japanese, Polish, Korean, Russian, Turkish, and Indonesian options)
- Responsive two-column layout (customizable to single column)
- Integrated analytics (Google Analytics GA4, Plausible.io, Busuanzi)
- Disqus comments support
- Category and tag organization
- RSS/Atom feeds
- Custom navigation with external links
- Blogroll section for linking to other blogs

## Special Tools & Scripts

- `_new_draft.sh` - Create new draft posts
- `_preview.sh` - Start local development server with drafts
- `_publish.sh` - Move draft to published posts with correct date
- Integration with `pangu` tool for Chinese typography
- Use of `tekorrect` for article formatting

The blog represents a long-term digital diary of the author's journey as a software engineer, athlete, and family person, documenting both technical and personal growth over nearly two decades.