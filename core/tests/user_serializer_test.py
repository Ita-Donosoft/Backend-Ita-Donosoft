import datetime

from core.models import User

from helpers import DefaultTestClass

from core.serializers import user_serializers


class UserSerializerTests(DefaultTestClass):
    def test_create_user_serializer(self):
        serializer_class = user_serializers.CreateUserSerializer

        validated_data = {
            'rut': '111111111',
            'name': 'user_name',
            'lastname': 'user_lastname',
            'email': 'user@domain.com',
            'role': 1,
            'profession': 'user_profession',
            'birth_date': '1999-03-12',
            'password': 'user_password'
        }

        serialzed_user = serializer_class(data=validated_data)
        serialzed_user.is_valid()
        serialzed_user.save()

        user_model = User.objects.get(id=1)

        created_user_data = {
            'id': user_model.id,
            'rut': user_model.rut,
            'name': user_model.name,
            'lastname': user_model.lastname,
            'email': user_model.email,
            'role': user_model.role,
            'profession': user_model.profession,
            'birth_date': user_model.birth_date.strftime('%Y-%m-%d'),
        }

        self.assertEqual(serialzed_user.data, created_user_data)
