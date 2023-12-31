from django.urls import path
from . import views

urlpatterns = [
    path('view-cart/', views.view_cart, name='view_cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('finalize_order/', views.finalize_order, name='finalize_order'),
]
