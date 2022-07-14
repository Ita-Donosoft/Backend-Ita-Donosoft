import datetime
import json

from rest_framework.test import APIClient

from helpers import DefaultTestClass


class AddEmployeeTests(DefaultTestClass):
    endpoint_url = '/api/secretary/addemployee'

    employee_data_to_create = {
        'rut': '333333333',
        'email': 'employee_2@domain.com',
        'name': 'employee_2_name',
        'lastname': 'employee_2_lastname',
        'profession': 'employee_2_profession',
        'birth_date': '1990-01-01',
        'role': '1',
        'password': 'employee_2_password'
    }

    def setUp(self):
        self.create_user({
            'rut': '111111111',
            'email': 'employee_1@domain.com',
            'name': 'employee_1_name',
            'lastname': 'employee_1_lastname',
            'profession': 'employee_1_profession',
            'role': 1,
            'birth_date': datetime.date(1990, 4, 3),
            'password': 'employee_1_password'
        })

        self.create_user({
            'rut': '222222222',
            'email': 'secretary@domain.com',
            'name': 'secretary_name',
            'lastname': 'secretary_lastname',
            'profession': '',
            'role': 2,
            'birth_date': datetime.date(1999, 4, 3),
            'password': 'secretary_password'
        })

    def test_add_employee_unauth(self):
        client = APIClient()
        response = client.post(
            self.endpoint_url,
            self.employee_data_to_create,
            format='json'
        )

        self.assertEqual(json.loads(response.content), {
            'detail': 'Authentication credentials were not provided.'
        })

    def test_add_employee_wrong_role(self):
        client = APIClient()
        token = self.login(
            '111111111', 'employee_1@domain.com', 'employee_1_password'
        )
        client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        response = client.post(
            self.endpoint_url,
            self.employee_data_to_create,
            format='json'
        )

        self.assertEqual(json.loads(response.content), {
            'error': 'The user must be a secretary'
        })

    def test_add_employee_no_data(self):
        client = APIClient()
        token = self.login(
            '222222222', 'secretary@domain.com', 'secretary_password'
        )
        client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        response = client.post(
            self.endpoint_url,
            {},
            format='json'
        )

        self.assertEqual(json.loads(response.content), {
            'errors': {
                'rut': [
                    'This field is required.'
                ],
                'email': [
                    'This field is required.'
                ],
                'name': [
                    'This field is required.'
                ],
                'lastname': [
                    'This field is required.'
                ],
                'birth_date': [
                    'This field is required.'
                ],
                'role': [
                    'This field is required.'
                ],
                'profession': [
                    'This field is required.'
                ],
                'password': [
                    'This field is required.'
                ]
            }
        })

    def test_add_employee_exists_rut(self):
        client = APIClient()
        token = self.login(
            '222222222', 'secretary@domain.com', 'secretary_password'
        )
        client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        response = client.post(
            self.endpoint_url,
            {
                'rut': '111111111',
                'email': 'employee_2@domain.com',
                'name': 'employee_2_name',
                'lastname': 'employee_2_lastname',
                'profession': 'employee_2_profession',
                'birth_date': '1990-01-01',
                'role': '1',
                'password': 'employee_2_password'
            },
            format='json'
        )

        self.assertEqual(json.loads(response.content), {
            'errors': {
                'rut': [
                    'This field must be unique.'
                ],
            }
        })

    def test_add_employee_exists_email(self):
        client = APIClient()
        token = self.login(
            '222222222', 'secretary@domain.com', 'secretary_password'
        )
        client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        response = client.post(
            self.endpoint_url,
            {
                'rut': '333333333',
                'email': 'employee_1@domain.com',
                'name': 'employee_2_name',
                'lastname': 'employee_2_lastname',
                'profession': 'employee_2_profession',
                'birth_date': '1990-01-01',
                'role': '1',
                'password': 'employee_2_password'
            },
            format='json'
        )

        self.assertEqual(json.loads(response.content), {
            'errors': {
                'email': [
                    'This field must be unique.'
                ],
            }
        })

    def test_add_employee_wrong_rut(self):
        client = APIClient()
        token = self.login(
            '222222222', 'secretary@domain.com', 'secretary_password'
        )
        client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        response = client.post(
            self.endpoint_url,
            {
                'rut': 'abcdefghijk',
                'email': 'employee_2@domain.com',
                'name': 'employee_2_name',
                'lastname': 'employee_2_lastname',
                'profession': 'employee_2_profession',
                'birth_date': '1990-01-01',
                'role': '1',
                'password': 'employee_2_password'
            },
            format='json'
        )

        self.assertEqual(json.loads(response.content), {
            'error': 'The rut format is wrong. Use the rut without symbols. If the check digit is K, use it in lower case'
        })

    def test_add_employee(self):
        client = APIClient()
        token = self.login(
            '222222222', 'secretary@domain.com', 'secretary_password'
        )
        client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        response = client.post(
            self.endpoint_url,
            self.employee_data_to_create,
            format='json'
        )
        new_employee_data = self.employee_data_to_create
        new_employee_data['id'] = 3
        self.assertEqual(json.loads(response.content), {
            'data': {
                'id': 3,
                'rut': '333333333',
                'email': 'employee_2@domain.com',
                'name': 'employee_2_name',
                'lastname': 'employee_2_lastname',
                'profession': 'employee_2_profession',
                'birth_date': '1990-01-01',
                'role': 1,
            }
        },
        )
