FROM python:3.11-slim

# Avoid .pyc
ENV PYTHONDONTWRITEBYTECODE=1
# No buffer for outputs
ENV PYTHONUNBUFFERED=1

# Dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    libpq-dev gcc python3-dev musl-dev \
    netcat-openbsd \
    && apt-get clean


# cd in the app dir
WORKDIR /app

# Copying required files 
COPY requirements.txt .
COPY requirements-dev.txt .
COPY app /app/


# Python install
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install python-dotenv
RUN pip install -r requirements-dev.txt


# DEV
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# PROD 
# CMD ["gunicorn", "kart.wsgi:application", "--bind", "0.0.0.0:8000"]

