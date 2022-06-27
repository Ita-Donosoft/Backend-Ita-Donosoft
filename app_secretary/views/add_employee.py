from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from core.serializers import user_serializers
from rest_framework.permissions import IsAuthenticated

class AddEmployee(ObtainAuthToken):
    permission_classes = (IsAuthenticated,)
    serializer_class = user_serializers.CreateUserSerializer
    user_serializer_class = user_serializers.UserSerializer

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
        if serialized_user.data['role'] != 2: #secretary
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

        rut_only_number = new_employee.validated_data['rut'][:-1].isnumeric()
        rut_check_digit = new_employee.validated_data['rut'][-1] == 'k' or new_employee.validated_data['rut'][-1].isnumeric()
        if not rut_only_number or (rut_only_number and not rut_check_digit):
            return Response({
                'error': 'The rut format is wrong. Use the rut without symbols. If the check digit is K, use it in lower case'
            }, status=status.HTTP_400_BAD_REQUEST
            )

        new_employee.save()
        return Response({
            'data': new_employee.data
        }, status=status.HTTP_201_CREATED
        )

