# pull official base image
FROM python:3.8.3-alpine

# set work directory
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code

# SET ENVIRONMENT VARIABLES

# PYTHONDONTWRITEBYTECODE: Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1

# PYTHONUNBUFFERED: Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev mariadb-connector-c-dev \
    && apk add mysql-client \
    && pip install --upgrade pip \
    && pip install pymysql mysqlclient --no-cache-dir \
    && python3 -m pip install -r requirements.txt --no-cache-dir

COPY . /code
RUN chmod +x /code/* \
    && chmod 777 /code/entrypoint.sh

# STATIC FILE SERVING
RUN mkdir -p /vol/static \
    && mkdir -p /vol/media

RUN adduser -D user \
    && chmod -R 777 /vol \
    && chown -R user:user /vol

RUN python3 manage.py test -v 3

USER user

EXPOSE 8000
CMD ["sh","entrypoint.sh"]
