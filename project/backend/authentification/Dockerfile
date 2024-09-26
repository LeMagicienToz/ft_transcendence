FROM python:3.12-alpine

WORKDIR /app

COPY . /app
COPY requirements.txt /app

RUN apk add gcc musl-dev postgresql-client
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install django-cors-headers

EXPOSE 8080

CMD ["sh", "migrate.sh"]