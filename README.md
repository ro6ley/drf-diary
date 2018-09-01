[![Build Status](https://travis-ci.org/NaiRobley/drf-diary.svg?branch=master)](https://travis-ci.org/NaiRobley/drf-diary) [![Coverage Status](https://coveralls.io/repos/github/NaiRobley/drf-diary/badge.svg?branch=master)](https://coveralls.io/github/NaiRobley/drf-diary?branch=master)

# Diary

Diary is an online journal where users can pen down their thoughts and feelings. 

The building blocks are:

* Python 3
* Django 2.1
* PostgreSQL

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

## Prerequisites

You need the following to be able to run the project:
* Python 3 installed
* Virtualenv
* Postgres (9.4+)
* Docker (Optional)

## Setting Up for Development

These are instructions for setting up Diary API in development environment.

* prepare directory for project code and virtualenv:
```
  $ mkdir -p ~/drfdiary_project
  $ cd ~/drfdiary_project
```

* prepare virtual environment
  (with virtualenv you get pip, we'll use it soon to install requirements):
```
  $ virtualenv --python=python3 venv-drfdiary
  $ source venv-drfdiary/bin/activate
```

* check out project code:
```
  $ git clone https://github.com/NaiRobley/drf-diary.git
```

* install requirements (Django, ...) into virtualenv:
```
  $ pip install -r drf-diary/requirements.txt
```

* make sure PostgreSQL server is installed and running, create
  database "drfdiary_dev":
```
  $ psql --user postgres
  postgres=# create database drfdiary_dev;
```

* create database tables:
```
  $ cd ~/drfdiary_project/drf-diary/drfdiary
  $ ./manage.py migrate
  $ ./manage createsuperuser
```

* run development server:
```
  $ ./manage.py runserver
```

The site should now be running at `http://localhost:8080/docs`
To log into Django administration site as a super user,
visit `http://localhost:8080/admin`

## Database Configuration

Database configuration is stored in `drfdiary/settings.py`.
The default database engine is Postgres. 

To use SQLite update `drfdiary/settings.py` as follows:

```
  DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.sqlite3',
          'NAME': 'drfdiary_dev.db',
      }
  }
```


## Running the tests

To run the tests:

```
  $ cd ~/drfdiary_project/drf-diary/drfdiary
  $ ./manage.py test
```

## Docker Image

Alternatively, you can create a docker image for development as well. This image will contain an instance of the application running with django's development server using a sqlite database and can be used to quickly setup a development instance.

* Update the Database settings to use sqlite3:
  ```
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'drfdiary_dev.db',
        }
    }
  ```

* Run the following commands:
  ```
    # Build the Docker Image
    $ docker build -t drfdiary_dev .

    # Run it
    $ docker run -dt -p 8000:8000 drfdiary_dev
    
    # Get the Container ID for the next step
    $ docker ps | grep drfdiary_dev

    # Create a super user
    $ docker exec -it <container_id> python drfdiary/manage.py createsuperuser

    # View the documentation at 127.0.0.1:8000/docs 
  ```

## Built With

* [Django](https://www.djangoproject.com/) - The web framework used
* [Django REST Framework](http://www.django-rest-framework.org/) - The framework used to build the API

## Authors

* **Robley Gori** - *Initial work* - [Robley Gori](https://github.com/NaiRobley)

See also the list of [contributors](https://github.com/NaiRobley/drf-diary/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
