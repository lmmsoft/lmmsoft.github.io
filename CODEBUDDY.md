# CODEBUDDY.md

## Project Overview

This is a Jekyll-based personal blog with 19 years of content (2006-2025), hosted on GitHub Pages. The blog contains 437 articles covering ACM competitions, travel journals, IT career experiences, and personal reflections. Content is primarily in Chinese with multi-language interface support.

## Development Commands

### Local Development
- `_preview.sh` - Start Jekyll development server with drafts and future posts (port 4000)
- `make serve` - Docker-based local development server using Jekyll 3.8.5 (port 3000 or 4000)
- `make build` - Docker-based Jekyll build to verify site compilation
- `bundle exec jekyll serve --host 0.0.0.0 --port 4000 --drafts --future --watch` - Native Jekyll development server
- `bundle exec jekyll build` - Native Jekyll build for error checking

### Content Management
- `_new_draft.sh [filename]` - Create new draft from template in `_drafts/`
- `_publish.sh filename.md` - Move draft to `_posts/`, auto-add date prefix and handle git operations

### Content Quality Tools
- `pangu -f filename.md` - Format Chinese typography and spacing
- `tekorrect -f filename.md` - Apply text corrections
- Always run both tools before publishing to ensure content quality

## Architecture

### Content Structure
- **`_posts/`** - Published blog articles (437 files, spanning 2006-2025)
- **`_drafts/`** - Draft articles, includes template.markdown for new posts
- **`_layouts/`** - Jekyll templates (default, page, post)
- **`_includes/`** - Reusable components (header, footer, sidebar, analytics)
- **`_sass/`** - SCSS stylesheets
- **`images/`** - Images organized by article date and topic
- **`_markdown-to-wechat/`** - Custom WeChat publishing tool

### Navigation Pages
Root-level markdown files use prefixes to control menu order:
- `a_home.md`, `b_about.md`, `c_archives.md`, `d_category.md`, `e_tags.md`, `f_guestbook.md`, `f_list.md`

## Publishing Workflow

1. Create draft: `_new_draft.sh article-title`
2. Edit content in `_drafts/` directory
3. Preview: `_preview.sh` or `make serve`
4. Format: Apply `pangu -f filename.md` and `tekorrect -f filename.md` for Chinese content
5. Verify: Run `make build` to ensure no build errors
6. Publish: `_publish.sh filename.md` (automatically handles git add/mv operations)

## Important Conventions

### File Naming
- Articles must use format: `YYYY-MM-DD-title.md` (use hyphens, not underscores)
- YAML front matter date cannot be future time (Jekyll ignores future articles)

### Content Standards
- Add `<!--more-->` marker for homepage excerpt display
- Optimize large images (tinypng.com API integration available)
- Chinese content should be formatted with pangu/tekorrect tools

### Multi-language Support
Site supports Chinese, English, Japanese, Polish, Korean, Russian, Turkish, and Indonesian interfaces via `_config.yml` configuration.

## Analytics and Integrations
- Google Analytics 4
- Busuanzi page view statistics  
- Plausible.io alternative analytics
- Disqus comment system
- jekyll-feed for RSS/Atom feeds

## Commit Message Style
Follow existing pattern from git log: `ADD: ...`, `FIX: ...`, `CHORE: ...`
Example: `ADD: 港漂日记62：父亲节独自带娃`