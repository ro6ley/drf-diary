[![Build Status](https://travis-ci.org/NaiRobley/drf-diary.svg?branch=master)](https://travis-ci.org/NaiRobley/drf-diary)  [![Maintainability](https://api.codeclimate.com/v1/badges/06c3c3319e917da59cbc/maintainability)](https://codeclimate.com/github/NaiRobley/drf-diary/maintainability)  [![Coverage Status](https://coveralls.io/repos/github/NaiRobley/drf-diary/badge.png?branch=master)](https://coveralls.io/github/NaiRobley/drf-diary?branch=master)

# Diary

Diary is an online journal where users can pen down their thoughts and feelings. You can also use it to track your online reading list by adding links to read later and mark them as `read` once read for convenience.

The building blocks are:

* Python 3.5
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
  $ ./manage.py makemigrations
  $ ./manage.py migrate
  $ ./manage createsuperuser
```

* run development server:
```
  $ ./manage.py runserver
```

The site should now be running at `http://localhost:8080/`.

To log into Django administration site as a super user,
visit `http://localhost:8080/admin`

## Documentation

Once up and running the documentation is available at: `http://localhost:8080/docs`

The endpoints in summary:

| Endpoint                                                       | Functionality                      |
|:-------------------------------------------------------------- |:---------------------------------- |
| POST /api/v1/get-token/                                        | Obtain a token                     |
| **Accounts**                                                   |                                    |
| POST /api/v1/accounts/login/                                   | User Login                         |
| POST /api/v1/accounts/logout/                                  | User Logout                        |
| POST /api/v1/accounts/password/change/                         | Update user password               |
| POST /api/v1/accounts/password/reset/                          | Reset user password                |
| POST /api/v1/accounts/password/reset/confirm/                  | Reset user password                |
| POST /api/v1/accounts/registration/                            | User sign up                       |
| POST /api/v1/accounts/registration/verify-email/               | Email verification upon sign up    |
| GET /api/v1/accounts/user/                                     | Fetch a user's details             |
| PUT /api/v1/accounts/user/                                     | Update a user's details            |
| PATCH /api/v1/accounts/user/                                   | Partially update a user's details  |
| **Entries**                                                    |                                    |   
| GET /api/v1/entries/                                           | Fetch all entries                  |
| GET /api/v1/entries/<entryId>/                                 | Fetch a single entry               |
| POST /api/v1/entries/                                          | Create an entry                    |
| PUT /api/v1/entries/<entryId>/                                 | Modify an entry                    |
| DELETE /api/v1/entries/<entryId>/                              | Delete an entry                    |
| **Categories**                                                 |                                    |
| GET /api/v1/categories/                                        | Fetch all categories               |
| GET /api/v1/categories/\<categoryId>/                          | Fetch a single category            |
| POST /api/v1/categories/                                       | Create a category                  |
| PUT /api/v1/categories/\<categoryId>/                          | Modify a category                  |
| DELETE /api/v1/categories/\<categoryId>/                       | Delete a category                  |
| **Articles**                                                   |                                    |
| GET /api/v1/categories/\<categoryId>/articles/                 | Fetch all articles in a category   |
| GET /api/v1/categories/\<categoryId>/articles/\<articleID>/    | Fetch a single article             |
| POST /api/v1/categories/                                       | Create an article                  |
| PUT /api/v1/categories/\<categoryId>/articles/\<articleID>/    | Modify an article                  |
| DELETE /api/v1/categories/\<categoryId>/articles/\<articleID>/ | Delete an article                  |

## Database Configuration

Database configuration is stored in `drfdiary/settings/development.py`.
The default database engine is Postgres. 

To use SQLite, update `drfdiary/settings/development.py` as follows:

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
  $ ./manage.py test --settings=settings.testing
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
* [Django REST Auth](https://django-rest-auth.readthedocs.io/en/latest/) - Django-rest-auth provides a set of REST API endpoints for Authentication and Registration

## Authors

* **[Robley Gori](https://github.com/NaiRobley)** - *Initial work*

See also the list of [contributors](https://github.com/NaiRobley/drf-diary/contributors) who participated in this project.

## License

This project is licensed under the MIT License.
