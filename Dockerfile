FROM jekyll/jekyll:3.8.5

COPY Gemfile* ./

RUN jekyll build

ENTRYPOINT [ "jekyll" ]

CMD [ "build" ]