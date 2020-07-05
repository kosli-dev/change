FROM jekyll/builder AS builder

ENV JEKYLL_DATA_DIR=/tmp/jekyll

RUN mkdir -p $JEKYLL_DATA_DIR
RUN chown -R jekyll:jekyll $JEKYLL_DATA_DIR

COPY docs $JEKYLL_DATA_DIR
WORKDIR $JEKYLL_DATA_DIR
RUN jekyll build --trace

# Runtime image
FROM python:3.7-alpine

RUN apk update

RUN apk add build-base cmake libffi-dev

RUN apk add libgit2-dev=1.0.0-r0

# For testing purposes - remove from distribution
RUN apk add git

ENV FLASK_APP=server.py
WORKDIR /app/server
COPY server/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

EXPOSE 8001

RUN mkdir /cdb_data
COPY default_config /cdb_data/default_config

COPY server/ .

ENTRYPOINT [""]
CMD ["python", "server.py"]

# Copy static content and documentation
COPY static/ app/static/
COPY --from=builder /tmp/jekyll/_site app/static/docs
