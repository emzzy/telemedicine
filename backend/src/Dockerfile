FROM python:3.13-slim 

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
RUN apt-get update && apt-get install -y \
        build-essential \
        libpq-dev \
        python3-dev \
        gcc \
        curl \
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/
CMD daphne -b 0.0.0.0 -p 8000 teleapp.asgi:application
# CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]