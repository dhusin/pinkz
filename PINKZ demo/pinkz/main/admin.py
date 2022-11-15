from typing import OrderedDict
from django.contrib import admin
from .models import Product, CartProduct, Cart,Order,Wishlist,Review#,Order,OrderItem

admin.site.register(Product)
# admin.site.register(Order)
# admin.site.register(OrderItem)
admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(Order)
admin.site.register(Wishlist)
admin.site.register(Review)
