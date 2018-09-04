FROM python:3.5-alpine

MAINTAINER Robley Gori

EXPOSE 8000

RUN apk add --no-cache gcc postgresql-dev python3-dev musl-dev

ADD . /drf-diary

WORKDIR /drf-diary

RUN pip install -r requirements.txt

RUN python drfdiary/manage.py makemigrations

RUN python drfdiary/manage.py migrate

CMD [ "python", "drfdiary/manage.py", "runserver", "0.0.0.0:8000" ]
