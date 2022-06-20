from core import serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from core.serializers import user_serializers


class AddEmployee(APIView):
    permission_classes = ()
    serializer_class = user_serializers.CreateUserSerializer

    def post(self, request):
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
