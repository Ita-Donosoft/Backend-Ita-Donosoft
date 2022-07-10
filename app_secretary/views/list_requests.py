from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated

from core.serializers import (
    request_serializer,
    user_serializers
)
from core.models import Request


class ListRequests(ObtainAuthToken):
    permission_classes = (IsAuthenticated,)
    request_serializer_class = request_serializer.RequestSerializer
    user_serializer_class = user_serializers.UserSerializer

    def get(self, request):
        """
        This endpoint is to get all the available request in the system. 

        Args:
            request (class 'rest_framework.request.Request'): This is the data of the client request.

        Returns:
            Response:
            1.  If the user is not logged returns an error message with the status code 401.
            2.  If the role of the user is not a secretary returns an error with the status code 403.
            3.  If the user is correct, returns all the available requests in the system with the status code 200.
        """
        serialized_user = self.user_serializer_class(request.user)

        if serialized_user.data['role'] != 2:
            return Response({'error': 'The user most be a secretary'}, status=status.HTTP_403_FORBIDDEN)

        requests = Request.objects.filter(is_active=True)
        serialized_requests = self.request_serializer_class(
            requests, many=True
        )

        return Response({'data': serialized_requests.data}, status=status.HTTP_200_OK)
