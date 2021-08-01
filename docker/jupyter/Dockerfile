FROM jupyter/minimal-notebook:notebook-6.4.0

ARG HOST_UID=1000
ARG HOST_GID=1000
ARG PROJECT_DIR

USER root
RUN set -eux \
     && sudo apt update \
     && sudo apt install -y --no-install-recommends \
     nano \
     vim \
     less \
     && sudo rm -rf /var/lib/apt/lists/*

RUN set -eux \
    && rm /etc/localtime \
    && ln -s /usr/share/zoneinfo/Europe/Moscow /etc/localtime

RUN conda install --yes bqplot matplotlib keras

USER jovyan

ENV VIRTUAL_ENV=/home/jovyan/.venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install dependencies:
# COPY requirements.txt .
RUN pip install --upgrade pip
# RUN pip install -r requirements.txt


# setting APP_DIR:
ENV APP_DIR=/app
# WORKDIR $APP_DIR
WORKDIR $APP_DIR

# Run the application, override command in docker-compose.yml:
# COPY dull.py /dull.py

# CMD ["python", "/dull.py"]