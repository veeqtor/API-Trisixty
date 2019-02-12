from django.urls import path
from rest_framework_jwt.views import (obtain_jwt_token, refresh_jwt_token,
                                      verify_jwt_token)

urlpatterns = [
    path('token/', obtain_jwt_token, name='token'),
    path('token/refresh/', refresh_jwt_token, name='token_refresh'),
    path('token/verify/', verify_jwt_token, name='token_verify'),
]
