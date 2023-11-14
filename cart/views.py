from django.shortcuts import render, get_object_or_404, redirect
from .models import Cart, CartItem
from products.models import Product
from .models import Cart, CartItem, Order

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_id = request.session.get('cart_id')
    
    if cart_id:
        cart = Cart.objects.get(id=cart_id)
    else:
        cart = Cart.objects.create()
        request.session['cart_id'] = cart.id
        
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect('view_cart')

def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart.objects.get(id=request.session.get('cart_id'))
    cart_item = CartItem.objects.get(cart=cart, product=product)
    
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    
    return redirect('view_cart')

def view_cart(request):
    cart_id = request.session.get('cart_id')
    if cart_id:
        cart = Cart.objects.get(id=cart_id)
        cart_items = CartItem.objects.filter(cart=cart)
        for item in cart_items:
            item.total_price = item.product.price * item.quantity  # Calcula o preço total do item
    else:
        cart_items = []
    
    return render(request, 'view_cart.html', {'cart_items': cart_items})

def finalize_order(request):
    cart_id = request.session.get('cart_id')

    if cart_id:
        cart = Cart.objects.get(id=cart_id)
        new_order = Order.objects.create(total_amount=0)  # Crie a ordem sem um usuário
        total_price = 0

        for item in cart.items.all():
            total_price += 50

        new_order.total_amount = total_price
        new_order.save()

        cart.items.clear()  # Limpe o carrinho após a ordem 

        return render(request, 'order_confirmation.html', {'order': new_order})

    # Lógica adicional para lidar com o caso em que o carrinho não existe
    return render(request, 'error_page.html', {'error_message': 'O carrinho está vazio ou não existe.'})
