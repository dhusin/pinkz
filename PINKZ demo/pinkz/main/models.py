from distutils.command.upload import upload
from unicodedata import category
from django.db import models

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
    price = models.IntegerField()
    image = models.ImageField(null = True, blank= True, upload_to='images/')

    def __str__(self):
        return self. productName
    
