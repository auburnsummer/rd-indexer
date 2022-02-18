FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
  python3 \
  python3-pip \
  tmux \
  curl \
  jq \
  && rm -rf /var/lib/apt/lists/*

RUN pip install datasette

RUN mkdir /etc/ts /etc/logs

RUN curl --output /bin/typesense.tar.gz https://dl.typesense.org/releases/0.23.0.rc20/typesense-server-0.23.0.rc20-linux-amd64.tar.gz \
  && tar -xvf /bin/typesense.tar.gz --directory /bin

# Overmind

RUN curl --location --output /bin/overmind.gz https://github.com/DarthSim/overmind/releases/download/v2.2.2/overmind-v2.2.2-linux-amd64.gz \
  && gzip -d /bin/overmind.gz \
  && chmod +x /bin/overmind

# Caddy

RUN curl --location --output /bin/caddy.tar.gz https://github.com/caddyserver/caddy/releases/download/v2.4.6/caddy_2.4.6_linux_amd64.tar.gz \
  && tar -xvf /bin/caddy.tar.gz --directory /bin

RUN ls /bin

COPY . /app
WORKDIR /app

RUN sh setup_typesense.sh

EXPOSE 80

CMD ["overmind", "start"]




