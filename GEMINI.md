# Project Overview

This project is a personal blog built with Jekyll, a static site generator written in Ruby. The blog is hosted on GitHub Pages. The content is written in Markdown, and the site's appearance is controlled by HTML layouts and CSS.

## Key Technologies

*   **Jekyll:** The static site generator used to build the blog.
*   **Ruby:** The programming language Jekyll is written in. Dependencies are managed with Bundler and defined in the `Gemfile`.
*   **Markdown:** The format used for writing blog posts.
*   **HTML/CSS:** Used for the site's structure and styling.
*   **GitHub Pages:** The hosting platform for the blog.

# Building and Running

The project includes several shell scripts to streamline the development process.

*   **Previewing the site:** To preview the site locally, including drafts and future posts, run the following command:

    ```bash
    ./_preview.sh
    ```

    This will start a local web server at `http://0.0.0.0:4000/`.

*   **Building the site:** The `jekyll serve` command in the `_preview.sh` script also builds the site. For a production build, you can use:

    ```bash
    bundle exec jekyll build
    ```

# Development Conventions

## Creating New Posts

To create a new draft, use the `_new_draft.sh` script:

```bash
./_new_draft.sh <draft_name>.md
```

This will create a new Markdown file in the `_drafts` directory, pre-filled with a template, and open it in `vim`.

## Publishing Posts

To publish a draft, use the `_publish.sh` script with the path to the draft file:

```bash
./_publish.sh _drafts/<draft_name>.md
```

This script will:
1.  Add the file to the Git staging area.
2.  Rename and move the file to the `_posts` directory, using the date from the post's front matter to create the filename in the format `YYYY-MM-DD-draft_name.md`.

## Deployment

The site is deployed automatically by GitHub Pages whenever changes are pushed to the main branch. The `_publish.sh` script handles staging the new post, which can then be committed and pushed to deploy.
