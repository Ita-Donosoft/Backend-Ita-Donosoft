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
        1. The user most be logged.
        2. All fields of the serializer are required.
        3. The user most be a employee.
        4. The data from the request is most be the same as the user logged. 

        Args:
            request (class 'rest_framework.request.Request'):
                This class have the data and information of the request including the body and headers.

        Returns:
            Response:
                1. If the user is logged and the data is correct returns a success message with the response code 201.
                2. If the user is not logged, returns a error message with the response code 401.
                3. If the rol of the user is not a employee reutrns a error message with the response code 403.
                4. If the user is logged but the data is not correct returns a error message with the response code 400.
        """
        serialized_user = self.user_serializer_class(request.user)

        if serialized_user.data['role'] != 1:
            return Response({'error': 'The user most be a employee'}, status=status.HTTP_403_FORBIDDEN)

        request_data = self.request_data_serializer_class(data=request.data)

        if not request_data.is_valid():
            return Response({'errors': request_data.errors}, status=status.HTTP_400_BAD_REQUEST)

        if not self.__verify_request_user_data(request_data.data, serialized_user.data):
            return Response({
                'error': 'The data of request is not the same of the user.'
            }, status=status.HTTP_400_BAD_REQUEST)

        self.__create_new_request(request_data.data, serialized_user.data)

        return Response({'msg': 'the request was created successfully'}, status=status.HTTP_201_CREATED)

    def __verify_request_user_data(self, request_data, user_data):
        """
        This function is for verify the data of the request is the same at the user is logged.

        Args:
            request_data (dict): Is the data of the request.
            user_data (dict): Is the data of the logged user.

        Returns:
            bool: Returns True if the data is the same or Flase if the data is not the same.
        """
        request_verify_data = [
            request_data['rut'],
            request_data['name'],
            request_data['lastname']
        ]

        user_verify_data = [
            user_data['rut'],
            user_data['name'],
            user_data['lastname']
        ]

        return request_verify_data == user_verify_data

    def __create_new_request(self, request_data, user_data):
        """
        This function create a new request with the validated data of the request and logged user.

        Args:
            request_data (dict): Is the data of the request.
            user_data (dict): Is the data of the logged user.
        """
        new_request_data = {
            'type': request_data['type'],
            'reason': request_data['reason'],
            'employee': user_data['id']
        }

        new_request = self.create_request_serializer_class(
            data=new_request_data
        )

        new_request.is_valid()
        new_request.save()
