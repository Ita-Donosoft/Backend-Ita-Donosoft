import datetime
import json
from rest_framework.test import APIClient

from helpers import DefaultTestClass


class EmployeeReportTests(DefaultTestClass):
    endpoint_url = '/api/secretary/employee/report'

    def setUp(self):
        self.create_user({
            'rut': '111111111',
            'email': 'employee_1@domain.com',
            'name': 'employee_name_1',
            'lastname': 'employee_lastname_1',
            'profession': 'employee_profession_1',
            'role': 1,
            'birth_date': datetime.date(1990, 4, 3),
            'password': 'employee_password_1'
        })

        self.create_user({
            'rut': '222222222',
            'email': 'employee_2@domain.com',
            'name': 'employee_name_2',
            'lastname': 'employee_lastname_2',
            'profession': 'employee_profession_2',
            'role': 1,
            'birth_date': datetime.date(1990, 4, 3),
            'password': 'employee_password_2'
        })

        self.create_user({
            'rut': '333333333',
            'email': 'secretary@domain.com',
            'name': 'secretary_name',
            'lastname': 'secretary_lastname',
            'profession': '',
            'role': 2,
            'birth_date': datetime.date(1999, 4, 3),
            'password': 'secretary_password'
        })

    def test_employee_report_unauth(self):
        client = APIClient()
        id = 1
        response = client.get(
            self.endpoint_url + f'/{id}',
        )

        self.assertEqual(json.loads(response.content), {
            'detail': 'Authentication credentials were not provided.'
        })

    def test_employee_report_wrong_role(self):
        client = APIClient()
        token = self.login(
            '111111111', 'employee_1@domain.com', 'employee_password_1'
        )
        client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        id = 1
        response = client.get(
            self.endpoint_url + f'/{id}',
        )

        self.assertEqual(json.loads(response.content), {
            'error': 'The user must be a secretary'
        })

    def test_employee_report_wrong_employee_role(self):
        client = APIClient()
        token = self.login(
            '333333333', 'secretary@domain.com', 'secretary_password'
        )
        client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        id = 3
        response = client.get(
            self.endpoint_url + f'/{id}',
        )

        self.assertEqual(json.loads(response.content), {
            'error': f'There is not an employee with the ID {id}'
        })

    def test_employee_report_unexists(self):
        client = APIClient()
        token = self.login(
            '333333333', 'secretary@domain.com', 'secretary_password'
        )
        client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        id = 4
        response = client.get(
            self.endpoint_url + f'/{id}',
        )

        self.assertEqual(json.loads(response.content), {
            'error': f'There is not an employee with the ID {id}'
        })

    def test_employee_report(self):
        client = APIClient()
        token = self.login(
            '333333333', 'secretary@domain.com', 'secretary_password'
        )
        client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        id = 1
        response = client.get(
            self.endpoint_url + f'/{id}',
        )

        self.assertEqual(response.headers['Content-Type'], 'application/pdf')
