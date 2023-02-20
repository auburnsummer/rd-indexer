FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y ca-certificates

RUN apt-get update && apt-get install -y \
  python3 \
  python3-pip \
  tmux \
  curl \
  jq \
  tree \
  && rm -rf /var/lib/apt/lists/*

## Datasette ##
RUN pip install "datasette~=0.61.1"

## Typesense ##
RUN mkdir /etc/ts /etc/logs

RUN curl --output /bin/typesense.tar.gz https://dl.typesense.org/releases/0.24.0/typesense-server-0.24.0-linux-amd64.tar.gz \
  && tar -xvf /bin/typesense.tar.gz --directory /bin

## Overmind ##
RUN curl --location --output /bin/overmind.gz https://github.com/DarthSim/overmind/releases/download/v2.4.0/overmind-v2.4.0-linux-amd64.gz \
  && gzip -d /bin/overmind.gz \
  && chmod +x /bin/overmind

## Caddy ##
RUN curl --location --output /bin/caddy.tar.gz https://github.com/caddyserver/caddy/releases/download/v2.6.3/caddy_2.6.3_linux_amd64.tar.gz \
  && tar -xvf /bin/caddy.tar.gz --directory /bin

COPY . /app
WORKDIR /app

RUN cd ./typesense && sh setup_typesense.sh

RUN rm -f .overmind.sock

EXPOSE 8080

CMD ["overmind", "start"]




