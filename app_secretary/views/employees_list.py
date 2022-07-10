from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from core.serializers import user_serializers
from rest_framework.permissions import IsAuthenticated
from core.models import User


class ListEmployees (ObtainAuthToken):
    permission_classes = (IsAuthenticated,)
    serializer_class = user_serializers.UserSerializer

    def get(self, request):
        """this endpoint is to get the list of all the active employees

        Args:
            request (class 'rest_framework.request.Request'):
                This class adds the data and information of the request.

        Returns:
            Response:
            If the user is not logged it returns a 401 error.
            If the user is not logged as a secretary it returns a 403 error.
            If the data is correct it returns an answer will the list of the active employees.
        """

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
