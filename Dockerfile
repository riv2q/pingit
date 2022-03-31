# syntax=docker/dockerfile:1

FROM python:3.9.2
MAINTAINER Krystian Rozycki <rozycki.krystian@gmail.com>

WORKDIR pingit

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY src/pingit/ .

CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]
