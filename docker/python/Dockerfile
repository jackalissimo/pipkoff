FROM python:3.7-buster

ARG HOST_UID=1000
ARG HOST_GID=1000
ARG CI_PROJECT_DIR

RUN set -eux \
    && apt update \
    && apt install -y --no-install-recommends \
    less \
    nano \
    vim \
    && rm -rf /var/lib/apt/lists/* \
    && rm /etc/localtime \
    && ln -s /usr/share/zoneinfo/Europe/Moscow /etc/localtime

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install dependencies:
#COPY requirements.txt .
RUN pip install --upgrade pip
#RUN pip install -r requirements.txt
RUN pip install -i https://test.pypi.org/simple/ --extra-index-url=https://pypi.org/simple/ tinkoff-invest-openapi-client
RUN pip install flask==1.1.4

# setting User
RUN groupadd pipkoff -g 1000 && useradd pipkoff -u 1000 -g 1000 -m -s /bin/bash
USER pipkoff

# setting APP_DIR:
ENV APP_DIR=/app
WORKDIR $APP_DIR

# Run the application, override command in docker-compose.yml:
COPY dull.py /dull.py

CMD ["python", "/dull.py"]
