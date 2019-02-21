"""Module for urls"""

from django.contrib import admin
from django.urls import path, include
from user.views import home

BASE_VERSION = 'api/v1/'

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path(f'{BASE_VERSION}user/', include('user.api.urls'))
]
