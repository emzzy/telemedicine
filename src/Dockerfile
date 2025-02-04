# Set the python version as a build-time argument
# with Python 3.12 as the default
ARG PYTHON_VERSION=3.12-slim-bullseye
FROM python:${PYTHON_VERSION}

# Create a virtual environment
RUN python -m venv /opt/venv

# Upgrade pip
RUN pip install --upgrade pip

# Set Python-related environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create the mini vm's code directory
RUN mkdir -p /code

# Set the working directory to that same code directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt ./app

# copy the project code into the container's working directory
COPY ./src /app

# Install the Python project requirements
RUN pip install -r requirements.txt

ARG DJANGO_SECRET_KEY
ENV DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY}

ARG DJANGO_DEBUG=0
ENV DJANGO_DEBUG=${DJANGO_DEBUG}

# database isn't available during build
# run any other commands that do not need the database
# such as:
RUN python manage.py vendor_pull
RUN python manage.py collectstatic --noinput
# whitenoise -> s3

# set the Django default project name
ARG PROJ_NAME="teleapp"
