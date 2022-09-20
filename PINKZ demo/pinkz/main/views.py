from http.client import HTTPResponse
from django.shortcuts import render
from django.http import HttpResponse
from .models import Product

def home(request):
    context = {'products' : Product.objects.all()}

    return render(request, 'home.html', context)