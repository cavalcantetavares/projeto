FROM python:3.13
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

RUN apt-get update && apt-get upgrade -y && apt-get install -y libsqlite3-dev libpq-dev build-essential libldap2-dev libsasl2-dev tox lcov 
RUN pip install -U pip setuptools

COPY requirements.txt /code/
RUN pip install -r /code/requirements.txt

ADD . /code/
EXPOSE 8000