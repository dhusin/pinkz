from http.client import HTTPResponse
import json
from optparse import Values
import string
from unicodedata import category, name
from django.shortcuts import render,redirect,get_list_or_404
from django.views.generic import ListView,DetailView
from django.http import HttpResponse
from .models import Product,Cart,CartProduct,Order,Wishlist,Review#,OrderItem,Order
from django.http import JsonResponse
from django.utils import timezone

from django.db.models import Q
from django.core import serializers
import requests
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

#pdf gereration
from django.template.loader import get_template
from xhtml2pdf import pisa

def home(request):
    context = {'products' : Product.objects.all()}

    return render(request, 'home.html', context)

# quick view
def quickViewDetails(request, id):
    
    data =  serializers.serialize('json', Product.objects.filter(productId = id))
    return HttpResponse(data, content_type="application/json")
    

def productDetail(request, id):
    context = {'product' : Product.objects.get(productId = id),"reviews": Review.objects.filter(product = Product.objects.get(productId = id)).order_by("-id")[:4]}
    return render(request,'product-detail.html',context)


def productsList(request,cat):
    context = {'products' : Product.objects.all(),
                'category': cat}

    return render(request, 'product.html', context)
    
def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

# autocomplete
def getProductList(request):
    all_products =  list(Product.objects.all().values_list('productName', flat=True))
    return JsonResponse(all_products, safe=False)

# search result
def searchProduct(request):
    if request.method == "POST" :
        searchTerm = request.POST.get("search")
        if searchTerm == "":
            return redirect(request.META.get('HTTP_REFERER'))
        else:
             product = Product.objects.filter(Q(productName__contains = searchTerm) | Q(short_Description__contains = searchTerm))

             if product :
                return render(request,"product_search.html",{'products' : product})

    
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def add_to_cart(request,id):
    # item = get_list_or_404(Product, productId = id)
    # order_item = OrderItem.objects.get_or_create(item  = item)
    # order_qs = Order.objects.filter(user = request.user,ordered = False)
    # if order_qs.exists():
    #     order = order_qs[0]
    #     # check if the order item is in the order
    #     if order.items.filter(item__productId =item.productId).exists():
    #         order_item.quantity += 1
    #         order_item.save()
    #     else:
    #         order.items.add(order_item)

    # else:
    #     ordered_date = timezone.now()
    #     order = Order.objects.create(user = request.user, ordered_date= ordered_date)
    #     order.items.add(order_item)

    # return JsonResponse('success')
    no_of_items_in_cart = 0
    product = Product.objects.get(productId = id)
    cart_id = request.session.get('cart_id',None)
    print(cart_id)
    # if cart exisits then check for the product already exixts
    if cart_id:
        cart_obj = Cart.objects.get(id = cart_id)
        this_product_in_cart = cart_obj.cartproduct_set.filter(
                product=product)
        # if the same product already exixts update quantity and total
        if this_product_in_cart.exists():
            cartproduct = this_product_in_cart.last()
            cartproduct.quantity += 1
            cartproduct.subtotal += product.price
            cartproduct.save()
            cart_obj.total += product.price
            cart_obj.save()
        # else create the product and set the total
        else:
            cartproduct = CartProduct.objects.create(cart =cart_obj, product = product,rate = product.price,quantity = 1, subtotal = product.price)
            cart_obj.total += product.price
            cart_obj.save()
      
    else:
        cart_obj = Cart.objects.create(total = 0, customer = request.user)
        request.session["cart_id"] = cart_obj.id
        cartproduct = CartProduct.objects.create(cart =cart_obj, product = product,rate = product.price,quantity = 1, subtotal = product.price)
        cart_obj.total += product.price
        cart_obj.save()
        
    return HttpResponse("success")


def mini_cart_view(request):
    cart_id = request.session.get('cart_id',None)
    user = request.user.id
    # print(request.user.get_username)
    cart_details = {'products':[],'total':0}
    # print(cart_id)
    if cart_id:
        
        
        for a in Cart.objects.filter(id=cart_id):
            
            for b in CartProduct.objects.filter(cart=cart_id) :
                print(b.product.image)
                temp = {
                        'prod_img':str(b.product.image),
                        'prod_name':b.product.productName,
                        'quantity':b.quantity,
                        'price':b.product.price
                    }
                cart_details['products'].append(temp)
            cart_details['total']=a.total
        # print(cart_details)
        cart = cart_details
    else:
        cart = None
    return JsonResponse(cart_details, safe=False)


def shopping_cart(request):
    # cart_id = request.session.get("cart_id", None)
    # if cart_id:
    #     cart = Cart.objects.filter(id=cart_id)
    # else:
    #     cart = None
    # context = {'cart' : cart}
    # print(cart)
    cart_id = request.session.get('cart_id',None)
    cart_details = {'products':[],'total':0}
    # print(cart_id)
    if cart_id:
        
        
        for a in Cart.objects.filter(Q(id=cart_id)):
            
            for b in CartProduct.objects.filter(cart=cart_id) :
                # print(b.product.image)
                temp = {
                        'prod_img':str(b.product.image),
                        'prod_id':b.id,
                        'prod_name':b.product.productName,
                        'quantity':b.quantity,
                        'price':b.product.price,
                        "subtotal": b.product.price * b.quantity
                    }
                cart_details['products'].append(temp)
            cart_details['total']=a.total
        # print(cart_details)
        cart = cart_details
    return render(request,"shopping_cart.html",cart_details)

def ManageCart(request,p_id):
    print("this is manage cart")
    action = request.GET.get("action")
    print(action)
    cp_obj = CartProduct.objects.get(id=p_id)
    cart_obj = cp_obj.cart
    if action == "inc":
            cp_obj.quantity += 1
            cp_obj.subtotal += cp_obj.rate
            cp_obj.save()
            cart_obj.total += cp_obj.rate
            cart_obj.save()
    elif action == "dcr":
        cp_obj.quantity -= 1
        cp_obj.subtotal -= cp_obj.rate
        cp_obj.save()
        cart_obj.total -= cp_obj.rate
        cart_obj.save()
        if cp_obj.quantity == 0:
            cp_obj.delete()
    else:
        pass
    return HttpResponse("success")

from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags

def PlaceOrder(request,address):
    cart_id = request.session.get("cart_id")
    shipping_address = json.loads(address)
    cart_details = {'products':[]}
    if cart_id:
        cart_obj = Cart.objects.get(id=cart_id)
        order_obj = Order.objects.create(
            cart = cart_obj,
            ordered_by = shipping_address['name'],
            address = shipping_address["doorno"],
            pin = shipping_address["pin"],
            mobile1 = shipping_address["mobile1"],
            mobile2 =shipping_address["mobile2"],
            email = shipping_address["email"],
            subtotal =cart_obj.total,
            discount = 0,
            total =cart_obj.total,
            order_status = "Order Received"
        )
        del request.session['cart_id']
        
        

        for a in Cart.objects.filter(Q(id=cart_id)):
            
            for b in CartProduct.objects.filter(cart=cart_id) :
                # print(b.product.image)
                temp = {
                        'prod_img':str(b.product.image),
                        'category' : b.product.category,
                        'prod_id':b.id,
                        'prod_name':b.product.productName,
                        "prod_dec": b.product.short_Description,
                        'quantity':b.quantity,
                        'price':b.product.price,
                        "subtotal": b.product.price * b.quantity
                    }
                cart_details['products'].append(temp)
            total = a.total
        
        # print(cart_details['products'])
        
        

        # send order confirmation email
        template = render_to_string("order_email.html",{
            "order_no" : order_obj.id,
            "cart_products" : cart_details['products'],
            "sub_total" : total,
            "total" : total + 100,
            "shipping_address" : str(shipping_address["doorno"]+"  "+ shipping_address["pin"] +". ")

        })

        email = send_mail("Order received",strip_tags(template),settings.EMAIL_HOST_USER,[shipping_address["email"]],fail_silently=False,html_message=template)
        email = send_mail("Congrats You got an order from "+shipping_address['name'],strip_tags(template),settings.EMAIL_HOST_USER,["signout135@gmail.com"],fail_silently=False,html_message=template)
        

    return HttpResponse("success")


def CustomerProfile(request):
    context = {}
    customer = request.user.id
    orders = Order.objects.filter(cart__customer=customer).order_by("-id")
    context["orders"] = orders
    print(context)

    return render(request,"orderdetails.html",context)

@login_required
def add_to_wishlist(request,id):
    prod_check = Product.objects.get(productId = id)
    if prod_check: 
        if Wishlist.objects.filter(user = request.user, product = prod_check):
            return HttpResponse("Product already in wishlist :)")
        else:
            Wishlist.objects.create(user = request.user, product = prod_check)
            return HttpResponse("success")

    else:
        return HttpResponse("error")

@login_required(login_url='/accounts/login/')
def show_wishlist(request):
    wishlist = Wishlist.objects.filter(user = request.user)
    return render(request,"wishlist.html",{"wishlist": wishlist})

def delete_from_wishlist(request,id):
    prod_check = Product.objects.get(productId = id)
    if Wishlist.objects.filter(user = request.user, product = prod_check):
        Wishlist.objects.get(user = request.user, product = prod_check).delete()
        return HttpResponse("success")
    else:
        return HttpResponse("error")

def Add_comment(request):
    product = Product.objects.get(productId = request.GET["id"])
    comment = request.GET.get("comment")
    ratings = request.GET.get("ratings")
    Review(user = request.user, product = product, comment= comment, rate = ratings).save()
    return HttpResponse("success")