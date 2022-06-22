import datetime
import json
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from core.models import User


class MakeRequestTests(TestCase):
    def setUp(self):
        birth_date = datetime.date(1990, 4, 3)
        user_1 = User.objects.create(
            rut='111111111',
            email='employee@domain.com',
            name='employee_name',
            lastname='employee_lastname',
            profession='employee_profession',
            role=1,
            birth_date=birth_date
        )
        password = 'employee_password'
        user_1.set_password(password)
        user_1.save()

    def test_make_request_unauth(self):
        client = APIClient()
        response = client.post('/api/employee/makerequest', {
            'type': 1,
            'reason': 'my reason',
            'rut': '111111111',
            'email': 'employee@domain.com',
            'name': 'employee_name',
            'lastname': 'employee_lastname'
        }, format='json')

        self.assertEqual(json.loads(response.content), {
            'detail': 'Authentication credentials were not provided.'
        })

    def login(self):
        client = APIClient()
        client.post('/api/auth/login', {
            'username': 'employee@domain.com',
            'password': 'employee_password',
        }, format='json')
        user_model = User.objects.get(rut='111111111')
        token = Token.objects.get(user=user_model)
        return token.key

    def test_make_request_no_data(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Token {self.login()}')
        response = client.post('/api/employee/makerequest', {}, format='json')

        self.assertEqual(json.loads(response.content), {
            'errors': {
                'type': [
                    'This field is required.'
                ],
                'reason': [
                    'This field is required.'
                ],
                'rut': [
                    'This field is required.'
                ],
                'name': [
                    'This field is required.'
                ],
                'lastname': [
                    'This field is required.'
                ]
            }
        })

    def test_make_request_wrong_rut(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Token {self.login()}')
        response = client.post('/api/employee/makerequest', {
            'type': 1,
            'reason': 'my reason',
            'rut': '222222222',
            'email': 'employee@domain.com',
            'name': 'employee_name',
            'lastname': 'employee_lastname'
        }, format='json')

        self.assertEqual(json.loads(response.content), {
            'error': 'The rut of request is not the same of the user.'
        })

    def test_make_request_wrong_name(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Token {self.login()}')
        response = client.post('/api/employee/makerequest', {
            'type': 1,
            'reason': 'my reason',
            'rut': '111111111',
            'email': 'employee@domain.com',
            'name': 'employee_2_name',
            'lastname': 'employee_lastname'
        }, format='json')

        self.assertEqual(json.loads(response.content), {
            'error': 'The name of request is not the same of the user.'
        })

    def test_make_request_wrong_lastname(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Token {self.login()}')
        response = client.post('/api/employee/makerequest', {
            'type': 1,
            'reason': 'my reason',
            'rut': '111111111',
            'email': 'employee@domain.com',
            'name': 'employee_name',
            'lastname': 'employee_2_lastname'
        }, format='json')

        self.assertEqual(json.loads(response.content), {
            'error': 'The lastname of request is not the same of the user.'
        })

    def test_make_request(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Token {self.login()}')
        response = client.post('/api/employee/makerequest', {
            'type': 1,
            'reason': 'my reason',
            'rut': '111111111',
            'email': 'employee@domain.com',
            'name': 'employee_name',
            'lastname': 'employee_lastname'
        }, format='json')

        self.assertEqual(json.loads(response.content), {
            'msg': 'the request was created successfully'
        })
