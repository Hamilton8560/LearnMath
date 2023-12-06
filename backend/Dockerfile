FROM python:3.10-slim-buster

RUN apt update && apt upgrade -y apt && apt install -y sqlite3

ADD . /app
RUN mkdir -p /app/logs
WORKDIR /app

ADD requirements.txt /app
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

EXPOSE 3000

CMD ["gunicorn", "--bind", "0.0.0.0:3000", "run:app", "--timeout 30"]
