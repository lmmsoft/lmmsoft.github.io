JEKYLL_VERSION=3.8.5
build:
	docker run --rm --volume="$PWD:/srv/jekyll" -it jekyll/jekyll:${JEKYLL_VERSION} jekyll build
serve:
	docker run --name newblog --volume="$PWD:/srv/jekyll" -p 3000:4000 -it jekyll/jekyll:${JEKYLL_VERSION} jekyll serve --watch --drafts
	docker run --name myblog --volume="$PWD:/srv/jekyll" -p 4000:4000 -it jekyll/jekyll:$JEKYLL_VERSION jekyll serve --watch --drafts

