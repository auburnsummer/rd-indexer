FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
  python3 \
  python3-pip \
  tmux \
  curl \
  jq \
  && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install pipx
RUN python3 -m pipx ensurepath

RUN pipx install poetry