# pull official base image
FROM python:3.10.12-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1

# install psycopg2 dependencies
RUN apk update && apk add postgresql-dev


COPY requirements/base.txt base.txt
COPY requirements/production.txt production.txt

RUN pip install pip --upgrade  && pip install -r production.txt

RUN mkdir -p /home/app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/static
RUN mkdir $APP_HOME/media

WORKDIR $APP_HOME

COPY . .

RUN ["chmod", "+x", "/home/app/web/entrypoint.sh"]

ENTRYPOINT ["/home/app/web/entrypoint.sh"]

# Remove the package manager cache
RUN rm -rf /etc/apk/cache
