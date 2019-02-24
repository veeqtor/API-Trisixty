## Trixbuy-API.


[![CircleCI](https://circleci.com/gh/veeqtor/API-Trisixty.svg?style=svg&circle-token=e5afacb0ac6b14d6ede2965d7c8178e5e461ae63)](https://circleci.com/gh/veeqtor/API-Trisixty)
[![Maintainability](https://api.codeclimate.com/v1/badges/2c9b86cef0bbe52ddc5d/maintainability)](https://codeclimate.com/github/veeqtor/API-Trisixty/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/2c9b86cef0bbe52ddc5d/test_coverage)](https://codeclimate.com/github/veeqtor/API-Trisixty/test_coverage)


## Description

The **Trixbuy-api** is the backbone of an e-commerce platform for buying and selling of homemade wears in Nigeria.
The API documentation can be found here: 

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/ec2e3eb971309499cf94)


## Key Application features

1. Buys wears.
2. Be a vendor and sell wears.


# Table of Contents

- [Getting Started](#getting-started)
- [Technologies](#technologies)
- [Installation and Usage](#Setting-up-for-development)
- [Testing](#Running-tests-and-generating-report)
- [License](#license)

## Getting Started

This is a python API built with [**Django v2.1**](https://docs.djangoproject.com) and [**Dango Rest Framework**](https://www.django-rest-framework.org) framework. Authentication of users is done via [**JSON Web Tokens**](https://jwt.io/).

## Technologies

- `Python 3.6.5`

- [**Django v2.1**](https://docs.djangoproject.com)

- [**Dango Rest Framework**](https://www.django-rest-framework.org) 

- [**PostgreSQL**](https://www.postgresql.org/)

- [**Redis**](https://redis.io/)

- [**Celery**](http://docs.celeryproject.org)


### Setting up for development

-   Check that python 3 is installed:

    ```bash
    python --v
    >> Python 3.6.5
    ```


-   Install pipenv:

    ```bash
    brew install pipenv
    ```

-   Check pipenv is installed:
    ```bash
    pipenv --version
    >> pipenv, version 2018.11.26
    ```
-   Check that postgres is installed:

    ```bash
    postgres --version
    >> postgres (PostgreSQL) 10.5
    ```

-   Clone the Trixbuy-api repo and cd into it:

    ```bash
    git clone https://github.com/veeqtor/API-Trisixty.git
    ```

-   Install dependencies:

    ```
    pipenv install
    ```

-   Install dev dependencies to setup development environment:

    ```bash
    pipenv install --dev
    ```

-   Rename the .env.sample file to .env and update the variables accordingly:

-   Activate a virtual environment:

    ```bash
    pipenv shell
    ```

-   Apply migrations and create a superuser:

    ```bash
    python manage.py migrate  && python manage.py createsuperuser
    ```

-   Run the application:

    ```bash
    python manage.py runserver
    ```


-   Should you make changes to the database models, run migrations as follows:

    ```bash
    python manage.py makemigrations && python manage.py migrate
    ```


-   Deactivate the virtual environment once you're done:
    ```bash
    exit
    ```
    
-   Running Redis server:
    ```bash 
    sh redis.sh
    ```  
    Run the above command in the root project directory, this will install redis for you (if not already installed) and also run/start the redis server for the first time on your local machine.
  

##  Running Celery worker

  - Please endeavour to update the `.env` file with the following keys and the appropriate values:
       ```
      REDIS_HOST = '<Redis host>'
      REDIS_PORT = 'Redis Port'
      ```
  
   - In a new terminal tab run the Celery Message Worker with:
   
        ```bash
        celery worker -A src.celery --loglevel=info --concurrency=4
        ```

##  Running tests and generating report

   On command line run: 
   
   ```bash
   pytest
   ```

   To further view the lines not tested or covered if there is any, 

   An `htmlcov` directory will be created, get the `index.html` file by entering the directory and view it in your browser.


## Contribution guide

##### Contributing

All proposals for contribution must satisfy the guidelines in the product wiki.
When contributing to this repository, please first discuss the change you wish to make via issue, email, or any other method with the owners of this repository before making a change.This Project shall be utilising a [Pivotal Tracker board](https://www.pivotaltracker.com/n/projects/2227314) to track the work done.

## License

This project is authored by **Nwokeocha victor** and is licensed for your use, modification and distribution under the **MIT** license.
