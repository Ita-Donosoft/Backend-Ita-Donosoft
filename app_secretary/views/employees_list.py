from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from core.serializers import user_serializers
from rest_framework.permissions import IsAuthenticated
from core.models import User


class ListEmployees (ObtainAuthToken):
    permission_classes = (IsAuthenticated,)
    serializer_class = user_serializers.CreateUserSerializer

    def get(self, request):
        serialized_user = self.serializer_class(request.user)
        if serialized_user.data['role'] != 2:  # secretary
            return Response({
                'error': 'The user must be a secretary'
            }, status=status.HTTP_403_FORBIDDEN
            )

        users = User.objects.all().filter(is_active=True, role=1)
        serialized_users = self.serializer_class(users, many=True)
        return Response({
            'data': serialized_users.data
        }, status=status.HTTP_200_OK   
        )
