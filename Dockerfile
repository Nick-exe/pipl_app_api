FROM python:3.7-alpine
LABEL Nick Essien

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev
RUN apk add --update --no-cache  geos \
        proj \
        gdal \
        gdal-dev \
        geos-dev \
        g++ \
        gcc \
        libgdal-dev \
        binutils 
RUN pip install -r requirements.txt
RUN apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D user
USER user