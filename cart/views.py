from django.shortcuts import render, get_object_or_404, redirect
from products.models import Product
from .models import Cart, CartItem, Order, OrderItem
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import uuid


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
            item.total_price = item.product.price * item.quantity  
    else:
        cart_items = []
    
    return render(request, 'view_cart.html', {'cart_items': cart_items})

@csrf_exempt
def finalize_order(request):
    if request.method == 'POST':
        cart_id = request.session.get('cart_id')

        if cart_id:
            cart = Cart.objects.get(id=cart_id)
            new_order = Order.objects.create(total_amount=0)

            total_price = 0

            for item in cart.items.all():
                if hasattr(item, 'product') and hasattr(item.product, 'price'):
                    total_price += item.product.price * item.quantity
                    OrderItem.objects.create(order=new_order, product=item.product, quantity=item.quantity)

            new_order.total_amount = total_price
            new_order.order_number = str(uuid.uuid4())[:8]
            new_order.save()

            cart.items.clear()

            return JsonResponse({'order_number': new_order.order_number})
        else:
            return JsonResponse({'error': 'O carrinho está vazio ou não existe.'}, status=400)
    else:
        return JsonResponse({'error': 'Método não permitido'}, status=405)

from django.views.decorators.csrf import csrf_exempt

