from http.client import HTTPResponse
from django.shortcuts import render
from django.views.generic import ListView,DetailView
from django.http import HttpResponse
from .models import Product

def home(request):
    context = {'products' : Product.objects.all()}

    return render(request, 'home.html', context)

def productDetail(request, id):
    context = {'product' : Product.objects.get(productId = id)}
    return render(request,'product-detail.html',context)

class HomeView(ListView):
    model = Product
    template_name = 'home.html'

class ProductDetailVIew(DetailView):
    model = Product
    template_name = 'product-detail.html'
