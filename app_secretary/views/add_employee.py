from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from core.serializers import user_serializers


class AddEmployee(APIView):
    permission_classes = ()
    serializer_class = user_serializers.CreateUserSerializer

    def post(self, request):
        """this endpoint is for add an employee

        Args:
            request (class 'rest_framework.request.Request'): 
                This class adds the data and information of the request.

        Returns:
            Response: 
                If the data is not correct it returns an error. 
                In the contrary case it returns the data of the employee.
        """
        new_employee = self.serializer_class(data=request.data)
        if not new_employee.is_valid():
            return Response({
                'errors': new_employee.errors
            }, status=status.HTTP_400_BAD_REQUEST
            )

        new_employee.save()
        return Response({
            'data': new_employee.data
        }, status=status.HTTP_201_CREATED
        )
