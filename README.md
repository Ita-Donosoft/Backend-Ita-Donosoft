# Backend Ita Dono.SOFT

This project is an employee management API for DreamFactory company.

## Features

- Login endpoint
- Add employee endpoint
- Create resignation request (of platform or current employment) endpoint
- Formalize request (new contract or a redignations request) endpoint
- List requests endpoint
- List employees endpoint
- Generate a employee report endpoint

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
![image](https://user-images.githubusercontent.com/86853554/179031978-d1222f5a-ad2d-4e3e-834f-14b28235b94d.png)
