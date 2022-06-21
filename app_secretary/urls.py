from django.urls import path
from . import views

urlpatterns = [
    path('addemployee', views.AddEmployee.as_view()),
]
