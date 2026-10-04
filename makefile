RUBY_IMAGE ?= ruby:3.3.6-bookworm
BUNDLER_VERSION ?= 2.4.19
DOCKER_RUN = docker run --rm -e BUNDLE_FROZEN=true -v "$(CURDIR):/site" -w /site
JEKYLL = $(DOCKER_RUN) $(RUBY_IMAGE) bash -lc 'gem install bundler -v $(BUNDLER_VERSION) --no-document && bundle _$(BUNDLER_VERSION)_ install &&

.PHONY: build serve verify

build:
	$(JEKYLL) JEKYLL_ENV=production bundle _$(BUNDLER_VERSION)_ exec jekyll build'
	python3 scripts/verify_site.py _site

serve:
	$(DOCKER_RUN) -p 4000:4000 $(RUBY_IMAGE) bash -lc 'gem install bundler -v $(BUNDLER_VERSION) --no-document && bundle _$(BUNDLER_VERSION)_ install && bundle _$(BUNDLER_VERSION)_ exec jekyll serve --host 0.0.0.0 --port 4000 --watch --drafts'

verify:
	python3 scripts/verify_site.py _site
