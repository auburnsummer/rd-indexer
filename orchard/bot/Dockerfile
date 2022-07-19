# NOTE: this should be ran from parent folder, i.e.
# `docker build -t <some tag> -f ./orchard/bot/Dockerfile`

# export LITESTREAM_ACCESS_KEY_ID=XXX
 # export LITESTREAM_SECRET_ACCESS_KEY=XXX


#
#   -e LITESTREAM_ACCESS_KEY_ID \
  #  -e LITESTREAM_SECRET_ACCESS_KEY \
#
#

FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
  python3 \
  python3-pip \
  python3-venv \
  bash \
  curl \
  jq \
  && rm -rf /var/lib/apt/lists/*

RUN echo "hello world"
RUN curl -sSL https://install.python-poetry.org | python3 -

# prepend poetry to path
ENV PATH="/root/.local/bin:${PATH}"

ADD https://github.com/benbjohnson/litestream/releases/download/v0.3.8/litestream-v0.3.8-linux-amd64-static.tar.gz /tmp/litestream.tar.gz
RUN tar -C /usr/local/bin -xzf /tmp/litestream.tar.gz

COPY . /app
WORKDIR /app

RUN ls
RUN poetry install --no-dev

EXPOSE 8000

RUN chmod +x "./orchard/bot/run.sh"
CMD [ "./orchard/bot/run.sh" ]
