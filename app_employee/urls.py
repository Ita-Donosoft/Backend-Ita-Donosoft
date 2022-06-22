from django.urls import path
from . import views

urlpatterns = [
    path('makerequest', views.MakeRequest.as_view()),
]
