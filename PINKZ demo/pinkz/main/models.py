from distutils.command.upload import upload
from email.policy import default
from operator import truediv
from tkinter.tix import Tree
from unicodedata import category
from django.db import models
from django.conf import settings

CAREGORY_CHOICES = (
    ('01','Personalized'),
    ('02','ToysGifts'),
    ('03','Stationary')
)

ORDER_STATUS = (
    ("Order Received", "Order Received"),
    ("Order Processing", "Order Processing"),
    ("On the way", "On the way"),
    ("Order Completed", "Order Completed"),
    ("Order Canceled", "Order Canceled"),
) 

class Product(models.Model):
    productId = models.AutoField(primary_key=True,unique=True)
    productName = models.CharField(max_length=100)
    short_Description = models.TextField(null = True)
    Descroption = models.TextField(null = True)
    category = models.CharField(choices=CAREGORY_CHOICES,max_length=2)
    Weight = models.PositiveIntegerField(default=0)
    MAterial = models.CharField(max_length=100,null = True)
    Colors_Available = models.CharField(max_length=100,null = True)
    size_Available = models.CharField(max_length=100,null = True)
    price = models.FloatField()
    image = models.ImageField(null = True, blank= True, upload_to='images/')

    def __str__(self):
        return self. productName

    def get_category_products(category_id):
        try:
            obj = Product.objects.all()
            for i in obj:
                print(i.get_category_display)
            return True
        except Exception as e:
            return e


# class OrderItem(models.Model):
#     item = models.ForeignKey(Product,on_delete = models.CASCADE)
#     quantity = models.IntegerField(default = 1)

#     def __str__(self):
#         return f"{self.quantity} of {self.item.productName}"

# class Order(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
#     ordered = models.BooleanField(default=False)
#     items = models.ManyToManyField(OrderItem)
#     start_date = models.DateTimeField(auto_now_add = True)
#     ordered_date = models.DateTimeField()

#     def __str__(self):
#         return self.user.username

class Cart(models.Model):
    customer =models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE) 
    total = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "Cart: " + str(self.id)


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rate = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()

    def __str__(self):
        return "Cart: " + str(self.cart.id) + " CartProduct: " + str(self.id)





class Order(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    ordered_by = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    pin = models.PositiveIntegerField()
       
    mobile1 = models.CharField(max_length=10)
    mobile2 = models.CharField(max_length=10)
    email = models.EmailField(null=True, blank=True)
    subtotal = models.PositiveIntegerField()
    discount = models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    # payment_method = models.CharField(max_length=20, default="Cash On Delivery")
    # payment_completed = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return "Order: " + str(self.id)

class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE) 
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "wishlist: " + str(self.id)

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE) 
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    comment =models.TextField(max_length = 1000)
    rate = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Comment: " + str(self.id)
