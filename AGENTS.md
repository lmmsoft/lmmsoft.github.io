# Repository Guidelines

## Project Structure & Module Organization
- Content lives in `_posts/` (published) and `_drafts/` (work in progress); keep filenames `YYYY-MM-DD-slug.md` so Jekyll picks them up.
- Presentation assets sit in `_layouts/`, `_includes/`, `_sass/`, and `css/main.scss`; extend these partials instead of editing generated HTML.
- Root pages such as `a_home.md`, `b_about.md`, and `c_archives.md` control navigation order via their alphabetic prefixes—follow the pattern for new menu entries.
- Media belongs in `images/` or `attachments/`. Helper scripts and tooling, including `_markdown-to-wechat/` and `_new_draft.sh`, stay versioned beside the content for repeatable workflows.

## Build, Test, and Development Commands
- `bundle install` – sync Ruby gems locally before running any Jekyll task.
- `bundle exec jekyll build` – run the static build to verify Liquid templates, front matter, and includes.
- `bundle exec jekyll serve --host 0.0.0.0 --port 4000 --drafts --future --watch` – mirror `_preview.sh` for live previews with drafts and scheduled posts.
- `make build` / `make serve` – execute the same build and preview inside `jekyll/jekyll:3.8.5` Docker containers when Ruby is unavailable.

## Coding Style & Naming Conventions
- YAML front matter uses two-space indentation and must declare `layout`, `title`, `date`, `categories` or `tags` as needed.
- Markdown favors semantic headings, fenced code blocks, and a single `<!--more-->` marker for excerpts. Run `pangu -f` and `tekorrect -f` before publishing Chinese prose.
- Sass files prefer four-space indentation, single quotes, and shared variables kept within `_sass/` partials that `css/main.scss` imports.

## Testing Guidelines
- Treat `bundle exec jekyll build` (locally or via `make build`) as the gatekeeper; the build must complete without warnings.
- Run `jekyll doctor` after upgrading gems or editing `_config.yml` to spot deprecated settings early.
- Draft workflow: scaffold with `_new_draft.sh`, preview through `_preview.sh`, and convert using `_publish.sh` to move dated drafts into `_posts/`.

## Commit & Pull Request Guidelines
- Follow the concise `ADD: …`, `FIX: …`, `CHORE: …` prefix style visible in `git log`; example: `ADD: toc 悬浮`.
- Keep commits focused and include generated assets only when required by the change.
- Pull requests should summarize the intent, note commands executed (`jekyll build`, `make serve`, etc.), link related issues or articles, and attach screenshots when the UI shifts.


压缩图片：

发布文章前，我都会用这个脚本，压缩目录里的图片，请修改最后的目录名，然后帮我运行这个脚本

/Users/lmm333/code/children/_markdown-to-wechat/tinypng.py