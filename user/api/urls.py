from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('register/', views.UserRegister.as_view(), name='register'),
    path('login/', views.UserLogin.as_view(), name='login'),
    path('verify/', views.UserAccountVerification.as_view(), name='verify'),
    path('verify/token/resend/', views.UserVerificationTokenResend.as_view(),
         name='resend_token'),
    path('password/reset', views.UserPasswordReset.as_view(),
         name='reset_password'),

]
