import datetime
import json
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from core.models import User


class MakeRequestTests(TestCase):
    def create_user(self, data):
        user = User.objects.create(
            rut=data['rut'],
            email=data['email'],
            name=data['name'],
            lastname=data['lastname'],
            profession=data['profession'],
            role=data['role'],
            birth_date=data['birth_date']
        )
        user.set_password(data['password'])
        user.save()
    
    def login(self, rut, email, password):
        client = APIClient()
        client.post('/api/auth/login', {
            'username': email,
            'password': password,
        }, format='json')
        user_model = User.objects.get(rut=rut)
        token = Token.objects.get(user=user_model)
        return token.key
    
    def setUp(self):
        self.create_user({
            'rut': '111111111',
            'email': 'employee@domain.com',
            'name': 'employee_name',
            'lastname': 'employee_lastname',
            'profession': 'employee_profession',
            'role': 1,
            'birth_date': datetime.date(1990, 4, 3),
            'password': 'employee_password'
        })


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

    def test_make_request_no_data(self):
        client = APIClient()
        token = self.login('111111111', 'employee@domain.com', 'employee_password')
        client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
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
        token = self.login('111111111', 'employee@domain.com', 'employee_password')
        client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        response = client.post('/api/employee/makerequest', {
            'type': 1,
            'reason': 'my reason',
            'rut': '222222222',
            'email': 'employee@domain.com',
            'name': 'employee_name',
            'lastname': 'employee_lastname'
        }, format='json')

        self.assertEqual(json.loads(response.content), {
            'error': 'The data of request is not the same of the user.'
        })

    def test_make_request_wrong_name(self):
        client = APIClient()
        token = self.login('111111111', 'employee@domain.com', 'employee_password')
        client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        response = client.post('/api/employee/makerequest', {
            'type': 1,
            'reason': 'my reason',
            'rut': '111111111',
            'email': 'employee@domain.com',
            'name': 'employee_2_name',
            'lastname': 'employee_lastname'
        }, format='json')

        self.assertEqual(json.loads(response.content), {
            'error': 'The data of request is not the same of the user.'
        })

    def test_make_request_wrong_lastname(self):
        client = APIClient()
        token = self.login('111111111', 'employee@domain.com', 'employee_password')
        client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        response = client.post('/api/employee/makerequest', {
            'type': 1,
            'reason': 'my reason',
            'rut': '111111111',
            'email': 'employee@domain.com',
            'name': 'employee_name',
            'lastname': 'employee_2_lastname'
        }, format='json')

        self.assertEqual(json.loads(response.content), {
            'error': 'The data of request is not the same of the user.'
        })

    def test_make_request(self):
        client = APIClient()
        token = self.login('111111111', 'employee@domain.com', 'employee_password')
        client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
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
