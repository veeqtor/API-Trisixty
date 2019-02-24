"""Module for urls"""

from django.contrib import admin
from django.urls import path, include
from user.views import home
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls

BASE_VERSION = 'api/v1/'

get_schema_view()
schema_view = get_schema_view(title='TrixBuy API',
                              description='An API enable user to register, '
                              'buy and sell clothes.')

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('schema/', schema_view),
    path('docs/', include_docs_urls(title='TrixBuy API',
                                    description='An API enable user to '
                                    'register, buy and sell clothes.')),
    path(f'{BASE_VERSION}user/', include('user.api.urls')),
]
