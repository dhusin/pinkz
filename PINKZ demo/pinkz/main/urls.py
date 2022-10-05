from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='Home'),
    path('product_detail/<id>/',views.productDetail,name="product_detail"),
]