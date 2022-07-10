from rest_framework import serializers

from core.models import (
    Request,
    User,
)
from .user_serializers import UserRequestSerializer


class RequestSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    type = serializers.IntegerField()
    reason = serializers.CharField()
    employee = UserRequestSerializer()

    class Meta:
        model = Request
        fields = '__all__'


class GetRequestDataSerializer(serializers.Serializer):
    type = serializers.IntegerField()
    reason = serializers.CharField()
    rut = serializers.CharField()
    name = serializers.CharField()
    lastname = serializers.CharField()

    class Meta:
        model = Request


class CreateRequestSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    type = serializers.IntegerField()
    reason = serializers.CharField()
    employee = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    def create(self, validated_data):
        return Request.objects.create(**validated_data)

    class Meta:
        model = Request
