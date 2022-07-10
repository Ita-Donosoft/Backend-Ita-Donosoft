from datetime import date, datetime
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated

from core.serializers import (
    request_serializer,
    user_serializers
)

from core.models import (
    Request,
    User
)

from helpers import send_mail


class FormalizeRequest(ObtainAuthToken):
    permission_classes = (IsAuthenticated,)
    request_serializer_class = request_serializer.RequestSerializer
    user_serializer_class = user_serializers.UserSerializer

    def get(self, request, id):
        """
        This endpoint is for get a specific request by id.

        Args:
            request (class 'rest_framework.request.Request'): This is the data of the client request.
            id (integer): Is the id of the searched request.

        Returns:
            Response:
            1.  If the user is not logged returns an error message with the status code 401.
            2.  If the role of the user is not a secretary returns an error with the status code 403.
            3.  If there is not a request with the id passed return an error with the status code 404.
            4.  If the user is logged in and exists a request with the id passed returns the request with the status code 200.
        """
        serialized_user = self.user_serializer_class(request.user)

        if serialized_user.data['role'] != 2:
            return Response({'error': 'The user most be a secretary'}, status=status.HTTP_403_FORBIDDEN)

        request_object = self.__get_request_object(id)

        if not request_object:
            return Response({'error': f'there is not a request with the id {id}'}, status=status.HTTP_404_NOT_FOUND)

        serialized_request = self.request_serializer_class(request_object)

        return Response({'data': serialized_request.data}, status=status.HTTP_200_OK)

    def post(self, request, id):
        """
        This endpoint is for formalize a request by sending an email to the employee who made it.
        Depending on the type of request the status of the employee who made it changes.

        Args:
            request (class 'rest_framework.request.Request'): This is the data of the client request.
            id (integer): Is the id of the request to formalize.

        Returns:
            Response:
            1.  If the user is not logged returns an error message with the status code 401.
            2.  If the role of the user is not a secretary returns an error with the status code 403.
            3.  If there is not a request with the id passed return an error with the status code 404.
            4.  If the user is correct and exists a request with the id passed 
            a message is returned informing that the mail was sent successfully with a status code 200.
        """
        serialized_user = self.user_serializer_class(request.user)

        if serialized_user.data['role'] != 2:
            return Response({'error': 'The user most be a secretary'}, status=status.HTTP_403_FORBIDDEN)

        request_object = self.__get_request_object(id)

        if not request_object:
            return Response({'error': f'there is not a request with the id {id}'}, status=status.HTTP_404_NOT_FOUND)

        serialized_request = self.request_serializer_class(request_object)
        employee_data = serialized_request.data['employee']

        self.__change_request_employee_state(request_object, employee_data)

        self.__send_email_to_employee(serialized_request.data, employee_data)

        return Response({'msg': 'the request was formalized successfully'}, status=status.HTTP_200_OK)

    def __get_request_object(self, id):
        """
        In this function a request is searched by its id 
        Args:
            id (integer): Is the id of the searched request.

        Returns:
            class 'Request': In case there is a request with the passed id its class is returned.
            None: If there is no request with the passed id, None is returned.
        """
        try:
            request_object = Request.objects.get(id=id)

        except Exception as e:
            print(e)
            request_object = None

        return request_object

    def __change_request_employee_state(self, request_instance, employee_data):
        """
        In this function, the request is deactivated and the status of the employee who made the request is changed.

        Args:
            request_instance (class 'Request'): Is the instance of the formalized request.
            employee_data (dict): is the data of the employee who made the request.
        """
        request_instance.is_active = False
        request_instance.save()
        employee = User.objects.get(rut=employee_data['rut'])

        if request_instance.type == 0:
            employee.in_service = 1

        elif request_instance.type == 1:
            employee.in_service = 0

        elif request_instance.type == 2:
            employee.in_service = False
            employee.is_active = False

        employee.save()

    def __send_email_to_employee(self, request_data, employee_data):
        email_data = {
            'name': employee_data['name'],
            'lastname': employee_data['lastname'],
            'request_date': datetime.strptime(request_data['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ'),
            'type': request_data['type'],
            'response_date': date.today()
        }

        send_mail(
            'Tu solicitud ha sido aceptada',
            email_data,
            'email/formalize_email.html',
            employee_data['email']
        )
