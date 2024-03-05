from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)
    singup_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    category = models.ForeignKey(Category,on_delete=models.RESTRICT)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True) # TexField permite textos de mas de 250 caracteres
    price = models.DecimalField(max_digits=9,decimal_places=2)
    singup_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="products",blank=True)

    def __str__(self):
        return self.name
    
from django.contrib.auth.models import User

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.RESTRICT)
    gender = models.CharField(max_length=1, default="M")
    phone = models.CharField(max_length=20)
    birthdate = models.DateField(null=True)
    address = models.TextField(max_length=50)

    def __str__(self):
        return self.user

class Order(models.Model):

    ORDER_STATUS = (
        ("0", "Required"),
        ("1", "Paid")
    )

    client = models.ForeignKey(Client, on_delete=models.RESTRICT)
    registration_date = models.DateTimeField(auto_now_add=True)
    order_number = models.CharField(max_length=20, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default="0")
    status = models.CharField(max_length=1, default="0", choices=ORDER_STATUS)

class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.RESTRICT)
    product = models.JSONField()
    cuantity = models.IntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.product.title