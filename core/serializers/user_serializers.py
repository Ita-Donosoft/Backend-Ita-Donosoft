from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from core.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'rut', 'email', 'name',
                  'lastname', 'role', 'profession', 'birth_date']


class CreateUserSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    rut = serializers.CharField(max_length=12, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(max_length=255, write_only=True)
    email = serializers.EmailField(max_length=255, validators=[UniqueValidator(queryset=User.objects.all())])
    name = serializers.CharField(max_length=50)
    lastname = serializers.CharField(max_length=50)
    profession = serializers.CharField(max_length=50, allow_blank=True, allow_null=True)
    birth_date = serializers.DateField()
    role = serializers.IntegerField()
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    class Meta:
        model = User
