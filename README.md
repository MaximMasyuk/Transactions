# Transactions appi


## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)

## General info
Simple Transactions appi create with DRF and postgresql

## Technologies
Project is created with:
* Django REST framework
* PostgreSQL

## Setup

* 1)Open the project in VsCode or PyCharm create the virtual environment with command 'python -m venv env' and activate it
* 2)In terminal you need run command 'pip install -r requirements.txt'
* 3)In postgressql create the compound for this database
* 4)Create file .env with db settings
* 6)In file sttings put your db settings
* 7)After that you need to run migrations with command 'python manage.py makemigrations' and 'python manage.py migrate'
* 8)And in the end you need to run command 'python manage.py runserver'
