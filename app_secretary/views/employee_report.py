from fileinput import filename
from logging import exception
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from yaml import serialize
from core.serializers import user_serializers
from core.models import User
from helpers import render_html_to_pdf

class EmployeeReport(ObtainAuthToken):
    permission_classes = (IsAuthenticated,)
    user_serializer_class = user_serializers.UserSerializer

    def get(self, request, id):
        serialized_user = self.user_serializer_class(request.user)
        if serialized_user.data['role'] != 2:
            return Response({'error': 'The user must be a secretary'}, status = status.HTTP_403_FORBIDDEN)

        employee_object = self.__get_employee_object(id)

        if not employee_object:
            return Response({
                'error': f'There is not an employee with the ID {id}'
            }, status = status.HTTP_404_NOT_FOUND)

        serialized_employee = self.user_serializer_class(employee_object)
        pdf = render_html_to_pdf('pdf/employee_report.html', serialized_employee.data)

        if not pdf:
            return HttpResponse('Not Found')

        response = HttpResponse(pdf, content_type = 'application/pdf')
        filename = '%s_Report.pdf' % (serialized_employee.data['name'])
        content = "inLine; filename='{filename}'"
        download = request.GET.get('download')

        if download:
            content = f"attachment; filename='{filename}'"
        response['Content-Disposition'] = content

        return response



    def __get_employee_object(self, id):
        try:
            employee_object = User.objects.get(id=id)
            if employee_object.role != 1:
                employee_object = None
            
        except Exception as e:
            print(e)
            employee_object = None 

        return employee_object

        
