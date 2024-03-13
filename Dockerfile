FROM python:3.10.12

LABEL authors="aashishnk"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

COPY . /app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python manage.py wait_for_db && python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]