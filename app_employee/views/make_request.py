from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated

from core.serializers import (
    request_serializer,
    user_serializers
)


class MakeRequest(ObtainAuthToken):
    permission_classes = (IsAuthenticated,)
    request_data_serializer_class = request_serializer.GetRequestDataSerializer
    create_request_serializer_class = request_serializer.CreateRequestSerializer
    user_serializer_class = user_serializers.UserSerializer

    def post(self, request):
        """
        This endpoint is for make a request only the user can make a request.
        The validation are:
        1. The user most be logged
        2. The data from the request is most be the same as the user logged 

        Args:
            request (class 'rest_framework.request.Request'):
                This class have the data and information of the request including the body and headers.

        Returns:
            Response:
                1. If the user is logged and the data is correct returns a success message with the response code 201.
                2. If the user is not logged, returns a error message with the response code 403.
                3. If the user is logged but the data is not correct returns a error message with the response code 400.
        """
        serialized_user = self.user_serializer_class(request.user)

        if serialized_user.data['role'] != 1:
            return Response({'error': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)

        request_data = self.request_data_serializer_class(data=request.data)

        if not request_data.is_valid():
            return Response({'errors': request_data.errors}, status=status.HTTP_400_BAD_REQUEST)

        serialized_user_request_data = [
            serialized_user.data['rut'],
            serialized_user.data['name'],
            serialized_user.data['lastname']
        ]

        request_data_verify = [
            request_data.data['rut'],
            request_data.data['name'],
            request_data.data['lastname']
        ]

        if serialized_user_request_data != request_data_verify:
            return Response({
                'error': 'The data of request is not the same of the user.'
            }, status=status.HTTP_400_BAD_REQUEST)

        new_request_data = {
            'type': request_data.data['type'],
            'reason': request_data.data['reason'],
            'employee': serialized_user.data['id']
        }

        new_request = self.create_request_serializer_class(data=new_request_data)

        if not new_request.is_valid():
            return Response({'errors': new_request.errors}, status=status.HTTP_400_BAD_REQUEST)

        new_request.save()

        return Response({'msg': 'the request was created successfully'}, status=status.HTTP_201_CREATED)
