FROM python:3.6-buster

ARG HOST_UID=1000
ARG HOST_GID=1000
ARG CI_PROJECT_DIR

RUN set -eux \
    && apt update \
    && apt install -y --no-install-recommends \
    nano \
    vim \
    && rm -rf /var/lib/apt/lists/* \
    && rm /etc/localtime \
    && ln -s /usr/share/zoneinfo/Europe/Moscow /etc/localtime

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install dependencies:
COPY requirements.txt .
RUN pip install -r requirements.txt

# setting APP_DIR:
ENV APP_DIR=/app
WORKDIR $APP_DIR

# Run the application, override command in docker-compose.yml:
COPY dull.py /dull.py

CMD ["python", "/dull.py"]
