from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('userapp.urls')),
    path('api/admin/', include('adminapp.urls')),
    path('api/agency/', include('agencyapp.urls'))
]
