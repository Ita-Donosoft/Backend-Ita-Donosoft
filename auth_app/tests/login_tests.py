import datetime
import json
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from core.models import User

from helpers import DefaultTestClass


class LoginTests(DefaultTestClass):
    def setUp(self):
        self.create_user({
            'rut': '111111111',
            'email': 'user@domain.com',
            'name': 'user_name',
            'lastname': 'user_lastname',
            'profession': 'user_1_profession',
            'role': 1,
            'birth_date': datetime.date(1990, 4, 3),
            'password': 'user_1_password',
        })

        self.create_user({
            'rut': '333333333',
            'email': 'user_3@domain.com',
            'name': 'user_name_3',
            'lastname': 'user_lastname_3',
            'profession': 'user_3_profession',
            'role': 1,
            'birth_date': datetime.date(1990, 4, 3),
            'password': 'user_3_password',
        })

    def test_login_successfully(self):
        client = APIClient()
        response = client.post('/api/auth/login', {
            'username': 'user@domain.com',
            'password': 'user_1_password',
        }, format='json')
        user_model = User.objects.get(rut='111111111')
        token = Token.objects.get(user=user_model)
        self.assertEqual(json.loads(response.content), {
            'data': {
                'token': token.key,
                'user': {
                    'id': 1,
                    'rut': '111111111',
                    'email': 'user@domain.com',
                    'name': 'user_name',
                    'lastname': 'user_lastname',
                    'role': 1,
                    'profession': 'user_1_profession',
                    'in_service': 0,
                    'birth_date': '1990-04-03'
                }
            }
        })

    def test_login_fail(self):
        client = APIClient()
        response = client.post('/api/auth/login', {
            'username': 'user_2@domain.com',
            'password': 'user_2_password',
        }, format='json')

        self.assertEqual(json.loads(response.content), {
            'errors': {
                'non_field_errors': ['Unable to log in with provided credentials.']
            }})

    def test_login_unavailable_user(self):
        client = APIClient()
        user = User.objects.get(id=2)
        user.is_active = False
        user.save()
        response = client.post('/api/auth/login', {
            'username': 'user_3@domain.com',
            'password': 'user_3_password',
        }, format='json')

        self.assertEqual(json.loads(response.content), {
            'errors': {
                'non_field_errors': ['Unable to log in with provided credentials.']
            }})
