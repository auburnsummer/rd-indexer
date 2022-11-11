FROM mcr.microsoft.com/devcontainers/base:jammy

RUN apt-get update && apt-get install -y \
  sudo \
  curl \
  wget \
  vim \
  git \
  git-lfs \
  python3-pip \
  pypy3 \
  python3-venv

RUN curl -L https://fly.io/install.sh | FLYCTL_INSTALL=/usr/local sh
RUN wget https://github.com/benbjohnson/litestream/releases/download/v0.3.9/litestream-v0.3.9-linux-amd64.deb
RUN dpkg -i litestream-v0.3.9-linux-amd64.deb

USER vscode
RUN python3 -m pip install --user pipx
ENV PATH="${PATH}:/home/vscode/.local/bin"
RUN pipx install poetry
