from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('register/', views.UserRegister.as_view(), name='register'),
    path('login/', views.LoginUser.as_view(), name='login')
]
