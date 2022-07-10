from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('auth_app.urls')),
    path('api/secretary/', include('app_secretary.urls')),
    path('api/employee/', include('app_employee.urls')),
]
