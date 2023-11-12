from django.db import models
from products.models import Product

class Cart(models.Model):
    # Chave estrangeira do CartItem relacionada a este Carrinho
    items = models.ManyToManyField(Product, through='CartItem', related_name='carts')

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)  # Chave estrangeira para o modelo Cart
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Chave estrangeira para o modelo Product
    quantity = models.PositiveIntegerField(default=1)
