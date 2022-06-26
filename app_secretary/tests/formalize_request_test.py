import datetime
import json
from rest_framework.test import APIClient

from core.models import (
    User,
    Request
)

from core.serializers import request_serializer

from helpers import DefaultTestClass


class FormalizeRequestTest(DefaultTestClass):
    endpoint_url = '/api/secretary/formalizerequest'
    serializer_class = request_serializer.RequestSerializer

    def setUp(self):
        user_1 = self.create_user({
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
            'email': 'secretary@domain.com',
            'name': 'secretary_name',
            'lastname': 'secretary_lastname',
            'profession': '',
            'role': 2,
            'birth_date': datetime.date(1999, 4, 3),
            'password': 'secretary_password'
        })

        self.create_request({
            'type': 0,
            'reason': 'request_1_reason',
            'employee': user_1
        })

        self.create_request({
            'type': 1,
            'reason': 'request_2_reason',
            'employee': user_1
        })

        self.create_request({
            'type': 2,
            'reason': 'request_3_reason',
            'employee': user_1
        })

    def test_get_request_to_formalize_unauth(self):
        client = APIClient()
        response = client.get(f'{self.endpoint_url}/1')
        self.assertEqual(json.loads(response.content), {
            'detail': 'Authentication credentials were not provided.'
        })

    def test_get_request_to_formalize_wrong_role(self):
        client = APIClient()
        token = self.login(
            '111111111', 'employee_1@domain.com', 'employee_password_1')
        client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        response = client.get(f'{self.endpoint_url}/1')

        self.assertEqual(json.loads(response.content), {
            'error': 'The user most be a secretary'
        })

    def test_get_request_to_formalize_wrong_id(self):
        client = APIClient()
        token = self.login(
            '222222222', 'secretary@domain.com', 'secretary_password')
        client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        response = client.get(f'{self.endpoint_url}/999')

        self.assertEqual(json.loads(response.content), {
            'error': 'there is not a request with the id 999'
        })

    def test_get_request_to_formalize(self):
        client = APIClient()
        token = self.login(
            '222222222', 'secretary@domain.com', 'secretary_password')
        client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        response = client.get(f'{self.endpoint_url}/1')

        request_1 = Request.objects.get(id=1)
        serialized_request_1 = self.serializer_class(request_1)

        self.assertEqual(json.loads(response.content), {
            'data': {
                'id': 1,
                'type': 0,
                'reason': 'request_1_reason',
                'employee': {
                    'rut': '111111111',
                    'email': 'employee_1@domain.com',
                    'name': 'employee_name_1',
                    'lastname': 'employee_lastname_1',
                    'profession': 'employee_profession_1',
                    'birth_date': '1990-04-03'
                },
                'created_at': serialized_request_1.data['created_at'],
                'is_active': True
            }
        })

    def test_formalize_request_unauth(self):
        client = APIClient()
        response = client.post(f'{self.endpoint_url}/1', format='json')
        self.assertEqual(json.loads(response.content), {
            'detail': 'Authentication credentials were not provided.'
        })

    def test_formalize_request_wrong_role(self):
        client = APIClient()
        token = self.login(
            '111111111', 'employee_1@domain.com', 'employee_password_1')
        client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        response = client.post(f'{self.endpoint_url}/1', format='json')

        self.assertEqual(json.loads(response.content), {
            'error': 'The user most be a secretary'
        })

    def test_formalize_request_wrong_id(self):
        client = APIClient()
        token = self.login(
            '222222222', 'secretary@domain.com', 'secretary_password')
        client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        response = client.post(f'{self.endpoint_url}/999', format='json')

        self.assertEqual(json.loads(response.content), {
            'error': 'there is not a request with the id 999'
        })

    def test_fotmalize_request_type_0(self):
        client = APIClient()
        token = self.login(
            '222222222', 'secretary@domain.com', 'secretary_password')
        client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        response = client.post(f'{self.endpoint_url}/1', format='json')

        self.assertEqual(json.loads(response.content), {
            'msg': 'the request was formalized successfully'
        })

        request = Request.objects.get(id=1)

        self.assertEqual(request.is_active, False)

        employee = User.objects.get(id=1)

        self.assertEqual(employee.in_service, True)

    def test_fotmalize_request_type_1(self):
        client = APIClient()
        token = self.login(
            '222222222', 'secretary@domain.com', 'secretary_password')
        client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        response = client.post(f'{self.endpoint_url}/2', format='json')

        self.assertEqual(json.loads(response.content), {
            'msg': 'the request was formalized successfully'
        })

        request = Request.objects.get(id=2)

        self.assertEqual(request.is_active, False)

        employee = User.objects.get(id=1)

        self.assertEqual(employee.in_service, False)

    def test_fotmalize_request_type_2(self):
        client = APIClient()
        token = self.login(
            '222222222', 'secretary@domain.com', 'secretary_password')
        client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        response = client.post(f'{self.endpoint_url}/3', format='json')

        self.assertEqual(json.loads(response.content), {
            'msg': 'the request was formalized successfully'
        })

        request = Request.objects.get(id=3)

        self.assertEqual(request.is_active, False)

        employee = User.objects.get(id=1)

        self.assertEqual(employee.in_service, False)
        self.assertEqual(employee.is_active, False)
