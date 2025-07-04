FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    git \
    libpq-dev gcc python3-dev musl-dev \
    && apt-get clean

# WORKDIR /app

# COPY . /app/

#COPY docker/iweb/entrypoint.sh /app/entrypoint.sh

RUN pip install --upgrade pip
RUN pip install -r requirements.txt 
RUN pip install python-dotenv

COPY docker/web/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]



# CMD production-ready avec Gunicorn
# CMD ["gunicorn", "kart.wsgi:application", "--bind", "0.0.0.0:8000"]

#RUN chmod +x /app/entrypoint.sh
#ENTRYPOINT ["/app/entrypoint.sh"]

