from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from core.serializers import user_serializers
from core.models import User
from helpers import render_html_to_pdf


class EmployeeReport(ObtainAuthToken):
    permission_classes = (IsAuthenticated,)
    user_serializer_class = user_serializers.UserSerializer

    def get(self, request, id):
        """This function creates a report for an employee with all his data.

        Args:
            request (rest_framework.request.Request):
                This var is all the data sended by the client.
            id (int): 
                This var is the unique ID of the employee.

        Returns:
            Response:
                If the ID of the employee is not correct it returns an 404 error.
                If the user is not logged it returns a 401 error.
                If the user is not logged as a secretary it returns a 403 error.
                If the data is correct it returns the data of the employee and 200 response and the PDF document.
        """
        serialized_user = self.user_serializer_class(request.user)
        if serialized_user.data['role'] != 2:
            return Response({'error': 'The user must be a secretary'}, status=status.HTTP_403_FORBIDDEN)

        employee_object = self.__get_employee_object(id)

        if not employee_object:
            return Response({
                'error': f'There is not an employee with the ID {id}'
            }, status=status.HTTP_404_NOT_FOUND)

        serialized_employee = self.user_serializer_class(employee_object)
        pdf = render_html_to_pdf(
            'pdf/employee_report.html', serialized_employee.data)

        if not pdf:
            return HttpResponse('Not Found')

        response = HttpResponse(pdf, content_type='application/pdf')
        filename = '%s_Report.pdf' % (serialized_employee.data['name'])
        content = "inLine; filename='{filename}'"
        download = request.GET.get('download')

        if download:
            content = f"attachment; filename='{filename}'"
        response['Content-Disposition'] = content

        return response

    def __get_employee_object(self, id):
        """This function try to get the instance of an employee.

        Args:
            id (int): 
                This var is the unique ID of the employee.

        Returns:
            class User:
                If the user instance is found and his role is employee, his instance is returned.
                If the role is not employee or the instance doesn't exist return None.
        """
        try:
            employee_object = User.objects.get(id=id)
            if employee_object.role != 1:
                employee_object = None

        except Exception as e:
            print(e)
            employee_object = None

        return employee_object
