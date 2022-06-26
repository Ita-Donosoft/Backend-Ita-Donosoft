from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from core.models import (
    User,
    Request
)


class DefaultTestClass(TestCase):
    def create_user(self, data):
        """
        In this function a user is created and saved in the test database.

        Args:
            data (dict): Is the data of the user to create,

        Returns:
            class 'User': Is the instance of the created user.
        """
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

        return user

    def create_request(self, data):
        """
        In this function a request is created and saved in the test database.

        Args:
            data (dict): Is the data of the request to create,

        Returns:
            class 'Request': Is the instance of the created request.
        """
        request = Request.objects.create(
            type=data['type'],
            reason=data['reason'],
            employee=data['employee'],
        )
        request.save()

    def login(self, rut, email, password):
        """
        In this function a user is logged in receiving his access token.

        Args:
            rut (str): is the rut of the user to logged.
            email (str): is the email of the user to logged.
            password (str): is the password of the user to logged.

        Returns:
            str: Returns the access token of the user.
        """
        client = APIClient()
        client.post('/api/auth/login', {
            'username': email,
            'password': password,
        }, format='json')
        user_model = User.objects.get(rut=rut)
        token = Token.objects.get(user=user_model)
        return token.key
