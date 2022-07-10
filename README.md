# Backend Ita Dono.SOFT

This project is an employee management API for DreamFactory company.

## Features

- Login endpoint
- Add employee endpoint
- Create resignation request (platform and current employment) endpoint
- Formalize request endpoint
- List requests endpoint
- List employees endpoin

## Technologies

### Programming lenguage

- Python

### Web framework

- Django
- django-rest-framework

## Documentation

[Click here to see the documentation of the endpoints](https://documenter.getpostman.com/view/19464642/UzBmPTwa)

## Installation

1. Clone the repo
2. Move to repo folder
3. Install dependencies with: `pip install -r requirements.txt`
4. Run migrations: `python manage.py migrate`
5. Run server: `python manage.py runserver`

## Test
- Run tests with: `python manage.py test -v 2`
- Run test coverage with: `coverage run manage.py test -v 2 && coverage report`

## Coverage report
![image](https://user-images.githubusercontent.com/86853554/176090128-f4edc3a4-2480-4598-a1ce-a9d878c283b7.png)
