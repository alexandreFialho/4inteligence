# pull official base image
FROM python:3.8

# set work directory
WORKDIR /webapp

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy requirements file
COPY ./requirements.txt /webapp

# install os dependencies
RUN \
    apt-get update \
    && pip install --upgrade pip setuptools wheel \
    && pip install -r /webapp/requirements.txt

# copy project
COPY ./app /webapp
COPY ./setup.py /webapp

RUN python setup.py install

ENTRYPOINT [ "/webapp/entrypoint.sh" ]