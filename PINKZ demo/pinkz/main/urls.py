from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='Home'),
    path('product_detail/<id>/',views.productDetail,name="product_detail"),
    path('product/<cat>/',views.productsList,name="product"),
    path('about',views.about,name="about"),
    path('contact',views.contact,name="contact"),
    # search call
    path('get_productslist',views.getProductList),
    path('searchProduct', views.searchProduct, name="searchProduct"),
    #quickview details
    path('quickViewDetails/<id>/',views.quickViewDetails,name='quickViewDetails'),

    # add tocart
    path('add_to_cart/<id>',views.add_to_cart,name = 'add_to_cart'),
    path('mini_cart_view',views.mini_cart_view,name="mini_cart_view"),
    path("shopping_cart",views.shopping_cart,name="shopping_cart"),
    path("manage_cart/<p_id>",views.ManageCart,name="manage_cart"),
    path("palce_order/<address>",views.PlaceOrder,name="palce_order"),
    path("customerProfile",views.CustomerProfile,name = "customerProfile"),
    path("add-to-wishlist/<id>/",views.add_to_wishlist,name="add-to-wishlist"),
    path("show_wishlist",views.show_wishlist,name="show_wishlist"),
    path("delete_from_wishlist/<id>", views.delete_from_wishlist,name = "delete_from_wishlist"),
    path("add_comment",views.Add_comment,name = "add_comment")
]