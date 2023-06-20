FROM nvidia/cuda:11.7.0-cudnn8-devel-ubuntu22.04

# Set timezone
ENV TZ=Asia/Tokyo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Set env
ENV PATH /root/.local/bin:$PATH
WORKDIR /app

# Instal libs
RUN apt update && \
    apt -y upgrade && \
    apt install --no-install-recommends -y \
    git make curl wget tar unzip direnv vim \
    build-essential libssl-dev libffi-dev

# Python
RUN apt install --no-install-recommends software-properties-common -y && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt update

RUN apt install --no-install-recommends -y \
    python3.11 python3.11-dev python3-pip

RUN ln -sf /usr/bin/python3.11 /usr/local/bin/python3 && \
    ln -sf /usr/bin/python3.11 /usr/local/bin/python && \
    pip install --upgrade pip setuptools

# Install poetry
# poetry installをDocker内でやると、volumeをマウントした際に消えるのでmakefileで実行
COPY . /app
RUN curl -sSL https://install.python-poetry.org | python3 -
RUN poetry run python -m pip install scikit-surprise # --use-pep517

# Clean
RUN apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
