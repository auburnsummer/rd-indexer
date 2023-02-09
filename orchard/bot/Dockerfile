FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
  python3 \
  python3-pip \
  python3-venv \
  tmux \
  wget \
  pypy3 \
  curl \
  jq \
  sqlite3 \
  && rm -rf /var/lib/apt/lists/*

RUN wget https://github.com/benbjohnson/litestream/releases/download/v0.3.9/litestream-v0.3.9-linux-amd64.deb --output-document /tmp/litestream.deb
RUN dpkg -i /tmp/litestream.deb

RUN python3 -m pip install pipx
RUN python3 -m pipx ensurepath

RUN pipx install poetry

ENV PATH=/root/.local/bin:$PATH

COPY . /app

WORKDIR /app

RUN poetry env use $(which pypy3)
RUN poetry install

ENV LITESTREAM_DB=/tmp/status.db
CMD [ "poetry", "run", "python", "-m", "orchard.bot", "/tmp/status.db" ]