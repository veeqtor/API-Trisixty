from django.shortcuts import render, HttpResponse

# Create your views here.


def home(request):
    """Home page"""
    return HttpResponse('Welcome !!.')

