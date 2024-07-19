# pull official base image
FROM python:alpine3.17

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# set display port to avoid crash
ENV DISPLAY=:99

# install dependencies
RUN pip install --upgrade pip
RUN pip install poetry
COPY ./pyproject.toml /usr/src/app/pyproject.toml
RUN poetry config --local virtualenvs.create false
RUN poetry install 

RUN apk add chromium

# copy project
COPY . .




