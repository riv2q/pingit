# syntax=docker/dockerfile:1
MAINTAINER Krystian Rozycki <rozycki.krystian@gmail.com>

FROM python:3.9.2

WORKDIR cisco-app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

# EXPOSE 8080
CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]
