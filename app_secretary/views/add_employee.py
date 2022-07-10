from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from core.serializers import user_serializers, request_serializer
from rest_framework.permissions import IsAuthenticated


class AddEmployee(ObtainAuthToken):
    permission_classes = (IsAuthenticated,)
    serializer_class = user_serializers.CreateUserSerializer
    user_serializer_class = user_serializers.UserSerializer
    request_serializer_class = request_serializer.CreateRequestSerializer

    def post(self, request):
        """this endpoint is for add an employee

        Args:
            request (class 'rest_framework.request.Request'): 
                This class adds the data and information of the request.

        Returns:
            Response: 
                If the data is not correct it returns an 400 error.
                If the user is not logged it returns a 401 error.
                If the user is not logged as a secretary it returns a 403 error.
                If the data is correct it returns the data of the employee and 201 response.
        """

        serialized_user = self.user_serializer_class(request.user)
        if serialized_user.data['role'] != 2:  # secretary
            return Response({
                'error': 'The user must be a secretary'
            }, status=status.HTTP_403_FORBIDDEN
            )

        new_employee = self.serializer_class(data=request.data)
        if not new_employee.is_valid():
            return Response({
                'errors': new_employee.errors
            }, status=status.HTTP_400_BAD_REQUEST
            )

        if(self.__verify_rut(new_employee.validated_data['rut'])):
            return Response({
                'error': 'The rut format is wrong. Use the rut without symbols. If the check digit is K, use it in lower case'
            }, status=status.HTTP_400_BAD_REQUEST
            )
        new_employee.save()

        self.create_new_contract(new_employee)

        return Response({
            'data': new_employee.data
        }, status=status.HTTP_201_CREATED
        )

    def create_new_contract(self, new_employee):
        """This function is for create a new contract for an employee

        Args:
            new_employee (CreateUserSerializer): This is the new employee
        """
        new_request = self.request_serializer_class(data={
            'type': 0,
            'reason':  'new contract',
            'employee': new_employee.data['id']
        }
        )
        new_request.is_valid()
        new_request.save()

    def __verify_rut(self, rut):
        """This function verify the format of the RUT.

        Args:
            rut (str): This is the RUT of the new employee.

        Returns:
            bool: 
            If the RUT is correct it returns True.
            In the contrary case it returns False.
        """
        rut_only_number = rut[:-1].isnumeric()
        rut_check_digit = rut[-1] == 'k' or rut[-1].isnumeric()

        return not rut_only_number or (rut_only_number and not rut_check_digit)
