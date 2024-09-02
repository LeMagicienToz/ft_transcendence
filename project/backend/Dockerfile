FROM python:3.12-alpine

WORKDIR /backend

COPY . /backend
COPY requirements.txt /backend

RUN apk add gcc musl-dev postgresql-client
RUN pip install --no-cache-dir -r /backend/requirements.txt

EXPOSE 8000

CMD ["sh", "migrate.sh"]