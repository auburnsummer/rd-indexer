FROM public.ecr.aws/lts/ubuntu:22.04_stable

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

# create a user, they can sudo for free
RUN useradd -rm -d /home/ada -s /bin/bash -g root -G sudo -u 1001 ada
RUN sh -c 'echo "ada ALL=(ALL:ALL) NOPASSWD: ALL"  | sudo tee /etc/sudoers.d/ada'
USER ada
WORKDIR /home/ada

RUN python3 -m pip install --user pipx
ENV PATH="${PATH}:/home/ada/.local/bin"

RUN pipx install poetry