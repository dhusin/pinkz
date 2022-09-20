from distutils.command.upload import upload
from django.db import models

class Product(models.Model):
    productId = models.AutoField(primary_key=True,unique=True)
    productName = models.CharField(max_length=100)
    productDesc = models.TextField()
    price = models.IntegerField()
    image = models.ImageField(null = True, blank= True, upload_to='images/')

    def __str__(self):
        return self. productName
    
