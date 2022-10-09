from distutils.command.upload import upload
from email.policy import default
from operator import truediv
from tkinter.tix import Tree
from unicodedata import category
from django.db import models
from django.conf import settings

CAREGORY_CHOICES = (
    ('01','Personalized'),
    ('02','Toys&Gifts'),
    ('03','Stationary')
)

class Product(models.Model):
    productId = models.AutoField(primary_key=True,unique=True)
    productName = models.CharField(max_length=100)
    productDesc = models.TextField()
    category = models.CharField(choices=CAREGORY_CHOICES,max_length=2)
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


class OrderItem(models.Model):
    item = models.ForeignKey(Product,on_delete = models.CASCADE)

    def __str__(self):
        return self.item

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    ordered = models.BooleanField(default=False)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add = True)
    ordered_date = models.DateTimeField()

    def __str__(self):
        return self.user.username
    
