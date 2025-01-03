from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from uuid import uuid4

class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()

    def __str__(self):
        return self.description

class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField()
    unit_price = models.DecimalField(max_digits=6,
                                     decimal_places=2,
                                     validators=[MinValueValidator(1)])
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['title']

class Customer(models.Model):

    phone = models.CharField(max_length=255) 
    birth_date = models.DateTimeField(null=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name

class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE)
    
    
class Order(models.Model):
    PAYMENT_STATUS_PENDING ='P'
    PAYMENT_STATUS_COMPLETE ='C'
    PAYMENT_STATUS_FAILED ='F'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_FAILED, 'Failed'),
        (PAYMENT_STATUS_COMPLETE, 'Complete')
    ]
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.placed_at)
    
    class Meta:
        permissions = [
            ('cancel_order', 'Can Cancel Order')
        ]

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT,related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return str(self.order.placed_at)

class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.id)

class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)]
    )

    def __str__(self):
        return str(self.cart.id)
    
    class Meta: #unique key
        unique_together = [['cart', 'product']]