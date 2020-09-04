# Multi-stage build to reduce image size
# See https://pythonspeed.com/articles/multi-stage-docker-python/
FROM python:3.8.5-slim as py

# Base
FROM py as base
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -y --no-install-recommends git\
    && rm -rf /var/lib/apt/lists/*

WORKDIR /mnutree

COPY .git ./.git
COPY setup.* ./
COPY src ./src

# Dev
FROM base as develop
COPY --from=base / /

RUN pip3 install --no-cache-dir -e . uvicorn

EXPOSE 8000

ENTRYPOINT ["uvicorn"]

# Production
FROM base as production
COPY --from=0 / /
COPY gunicorn_config.py ./

RUN pip3 install --no-cache-dir . gunicorn

CMD exec gunicorn mnuapi:app -c gunicorn_config.py