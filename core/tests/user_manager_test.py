import datetime

from core.models import User

from helpers import DefaultTestClass


class UserManagerTest(DefaultTestClass):

    def test_create_user(self):
        User.objects.create_user(
            rut='111111111',
            name='user_name',
            lastname='user_lastname',
            email='user@domain.com',
            role=1,
            profession='user_profession',
            birth_date='1999-03-12',
            password='user_password'
        )

        created_user = User.objects.get(id=1)

        created_user_data = {
            'rut': created_user.rut,
            'name': created_user.name,
            'lastname': created_user.lastname,
            'email': created_user.email,
            'role': created_user.role,
            'profession': created_user.profession,
            'birth_date': created_user.birth_date,
            'in_service': created_user.in_service,
            'is_active': created_user.is_active,
            'is_staff': created_user.is_staff
        }

        expected_user_data = {
            'rut': '111111111',
            'name': 'user_name',
            'lastname': 'user_lastname',
            'email': 'user@domain.com',
            'role': 1,
            'profession': 'user_profession',
            'birth_date': datetime.date(1999, 3, 12),
            'in_service': 0,
            'is_active': True,
            'is_staff': False
        }

        self.assertEqual(created_user_data, expected_user_data)

    def test_create_super_user(self):
        User.objects.create_superuser(
            rut='222222222',
            name='superuser_name',
            lastname='superuser_lastname',
            email='superuser@domain.com',
            role=0,
            birth_date='1999-03-12',
            password='superuser_password'
        )

        created_superuser = User.objects.get(id=1)

        created_superuser_data = {
            'rut': created_superuser.rut,
            'name': created_superuser.name,
            'lastname': created_superuser.lastname,
            'email': created_superuser.email,
            'role': created_superuser.role,
            'profession': created_superuser.profession,
            'birth_date': created_superuser.birth_date,
            'in_service': created_superuser.in_service,
            'is_active': created_superuser.is_active,
            'is_staff': created_superuser.is_staff
        }

        expected_superuser_data = {
            'rut': '222222222',
            'name': 'superuser_name',
            'lastname': 'superuser_lastname',
            'email': 'superuser@domain.com',
            'role': 0,
            'profession': None,
            'birth_date': datetime.date(1999, 3, 12),
            'in_service': 0,
            'is_active': True,
            'is_staff': True
        }

        self.assertEqual(created_superuser_data, expected_superuser_data)
