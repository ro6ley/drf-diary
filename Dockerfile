FROM python:3

MAINTAINER Robley Gori

EXPOSE 8000

ADD . /drf-diary

WORKDIR /drf-diary

RUN pip install -r requirements.txt

RUN python drfdiary/manage.py makemigrations

RUN python drfdiary/manage.py migrate

CMD [ "python", "drfdiary/manage.py", "runserver", "0.0.0.0:8000" ]
