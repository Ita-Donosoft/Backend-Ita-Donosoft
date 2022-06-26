import datetime
import json
from rest_framework.test import APIClient

from core.models import Request
from core.serializers import request_serializer

from helpers import DefaultTestClass


class ListRequestsTest(DefaultTestClass):
    endpoint_url = '/api/secretary/requests'
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

        user_2 = self.create_user({
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

        self.create_request({
            'type': 0,
            'reason': 'request_1_reason',
            'employee': user_1
        })

        self.create_request({
            'type': 1,
            'reason': 'request_2_reason',
            'employee': user_2
        })

    def test_list_requests_unatuh(self):
        client = APIClient()
        response = client.get(self.endpoint_url)

        self.assertEqual(json.loads(response.content), {
            'detail': 'Authentication credentials were not provided.'
        })

    def test_list_request_wrong_role(self):
        client = APIClient()
        token = self.login(
            '111111111', 'employee_1@domain.com', 'employee_password_1')
        client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        response = client.get(self.endpoint_url)

        self.assertEqual(json.loads(response.content), {
            'error': 'The user most be a secretary'
        })

    def test_list_requests(self):
        client = APIClient()
        token = self.login(
            '333333333', 'secretary@domain.com', 'secretary_password')
        client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        response = client.get(self.endpoint_url)

        request_1 = Request.objects.get(id=1)
        request_2 = Request.objects.get(id=2)
        serialized_request_1 = self.serializer_class(request_1)
        serialized_request_2 = self.serializer_class(request_2)

        self.assertEqual(json.loads(response.content), {
            'data': [
                {
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
                },
                {
                    'id': 2,
                    'type': 1,
                    'reason': 'request_2_reason',
                    'employee': {
                        'rut': '222222222',
                        'email': 'employee_2@domain.com',
                        'name': 'employee_name_2',
                        'lastname': 'employee_lastname_2',
                        'profession': 'employee_profession_2',
                        'birth_date': '1990-04-03',
                    },
                    'created_at': serialized_request_2.data['created_at'],
                    'is_active': True
                },
            ]
        })
