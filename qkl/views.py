from django.shortcuts import render, redirect


def index(request):
    return render(request, 'qkl/login.html')


def register(request):
    return render(request, 'qkl/register.html')

# Create your views here.
