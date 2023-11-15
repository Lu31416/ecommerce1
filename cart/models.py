from django.db import models
from products.models import Product
import uuid

class Cart(models.Model):
    # Chave estrangeira do CartItem relacionada a este Carrinho
    items = models.ManyToManyField(Product, through='CartItem', related_name='carts')

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)  # Chave estrangeira para o modelo Cart
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Chave estrangeira para o modelo Product
    quantity = models.PositiveIntegerField(default=1)


class Order(models.Model):
    order_number = models.CharField(max_length=8, unique=True, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

