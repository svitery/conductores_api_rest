from django.contrib import admin
from django.urls import path
from django.conf.urls import include,url
from rest_framework import routers
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'',include('datos.urls'))
]
