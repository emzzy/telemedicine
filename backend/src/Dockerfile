FROM python:3.13-alpine AS builder

RUN mkdir /app
WORKDIR /app
# Set Python-related environment variables
# Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
#Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

# Upgrade pip
RUN pip install --upgrade pip

# build pyscopg2-binary from source -- add required dependencies
RUN apk update && apk add --no-cache \
        gcc \
        musl-dev \
        libffi-dev \
        python3-dev \
        postgresql-dev \
        bash \
        && pip install --upgrade pip
        
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# run dev server
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]