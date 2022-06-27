from django.urls import path
from . import views

urlpatterns = [
    path('addemployee', views.AddEmployee.as_view()),
    path('requests', views.ListRequests.as_view()),
    path('formalizerequest/<id>', views.FormalizeRequest.as_view()),
    path('users', views.ListEmployees.as_view()),
]
