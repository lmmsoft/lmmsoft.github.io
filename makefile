JEKYLL_VERSION=3.8.5
DOCKER_TTY:=$(shell test -t 0 && echo -it)
build:
	docker run --rm --volume="$(CURDIR):/srv/jekyll" $(DOCKER_TTY) jekyll/jekyll:${JEKYLL_VERSION} jekyll build
serve:
	docker run --name newblog --volume="$(CURDIR):/srv/jekyll" -p 3000:4000 $(DOCKER_TTY) jekyll/jekyll:${JEKYLL_VERSION} jekyll serve --watch --drafts
	docker run --name myblog --volume="$(CURDIR):/srv/jekyll" -p 4000:4000 $(DOCKER_TTY) jekyll/jekyll:$JEKYLL_VERSION jekyll serve --watch --drafts
