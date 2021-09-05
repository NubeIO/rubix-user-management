ARG BASE_IMAGE_VERSION
FROM python:$BASE_IMAGE_VERSION-slim-buster as build

RUN apt update -qq \
    && apt install git curl gcc g++ make file musl-dev libffi-dev zlib1g zlib1g-dev -y \
    && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

WORKDIR /usr/src/app/
ADD poetry.lock pyproject.toml ./
RUN $HOME/.poetry/bin/poetry install

ADD src src
ADD config config
ADD migrations migrations
ADD run.py ./
RUN $HOME/.poetry/bin/poetry run pyinstaller run.py -n rubix-user-management --clean --onefile \
    --add-data pyproject.toml:. \
    --add-data config:config \
    --add-data migrations:migrations

FROM python:$BASE_IMAGE_VERSION-slim

ARG MAINTAINER="zero88 <sontt246@gmail.com>"
ARG APP_VERSION="1.0.0"
ARG RUBIX_UID=642
ARG NUBEIO_GID=1173
ARG COMMIT_SHA=$COMMIT_SHA

LABEL maintainer=$MAINTAINER version=$APP_VERSION commit=$COMMIT_SHA

ENV RUBIX_USER_MANAGEMENT_DATA=/data/rubix-user-management

RUN groupadd -g $NUBEIO_GID nubeio \
    && useradd -u $RUBIX_UID -G nubeio rubix \
    && mkdir -p $RUBIX_USER_MANAGEMENT_DATA \
    && chown -R rubix:nubeio $RUBIX_USER_MANAGEMENT_DATA

WORKDIR /usr/src/app/
COPY --chown=rubix:nubeio --from=build /usr/src/app/dist/rubix-user-management ./

USER rubix:nubeio

VOLUME $RUBIX_USER_MANAGEMENT_DATA

EXPOSE 1617

ENTRYPOINT [ "./rubix-user-management" ]
