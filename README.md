****An E-commerce StoreFront Application****
-
>A very robust storefront project. This is a well-structured, designed implementation of an online e-commerce application that is currently built with Django and Django REST Framework. This application has all the best practice using One2One, Many-2-One, Many-2-Many relationship and connecting separate apps using Generic Relationship. A robust  and rich API endpoints using viewsets and routers.

> The project is currently undergoing development with the aim of bringing rich features and ideas to uniquely identify Storefront.

## Features

- Django 4.0, Python 3.9, djangorestframework 3.13, drf-nested-routers 0.93 & django-filter 21.1
- Install via [Pipenv](https://pypi.org/project/pip/)
- User registration, login and logout (In Progress...)

The code style used for the project is PEP 8 -- Style Guide for Python Code and Flake8: For Style Guide
Enforcement.

---
## Table of Contents
* **[Installation](#installation)**
  * [Pipenv](#pip)
* [Setup](#setup)

---
## Installation
The application can be installed via Pipenv. To start,
clone the repo to your local computer and change into the proper directory.

```
$ git clone https://github.com/Fachiis/Storefront
$ cd Storefront
```
```
$ pipenv install
$ pipenv shell
(Storefront) $ python manage.py migrate
(Storefront) $ python manage.py createsuperuser
(Storefront) $ python manage.py runserver
# Load the site at http://127.0.0.1:8000/api/v1/
```

## Setup

```
# Run Migrations
(Storefront) $ python manage.py migrate

# Create a Superuser
(Storefront) $ python manage.py createsuperuser

# Confirm everything is working:
(Storefront) $ python manage.py runserver

# Load the site at http://127.0.0.1:8000/api/v1/
```
Enjoy the Storefront!