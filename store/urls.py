from django.urls import path
from .views import *
from store.models import *

urlpatterns = [
    path('/error',custom_404_view , name='error'),
    path('', home, name='home'),  # Home page route
    path('login', login_view, name='login'),
    path('register/',register_view, name='register'),
    path('profile/', profile, name='profile'),
    path('logout/', logout_view, name='logout'),
    path('product_list/',product_list, name='product_list'),
    path('product/<int:product_id>/',product_detail, name='product_detail'),
    path('add/<int:product_id>/',add_to_cart, name='add_to_cart'),
    path('cart/',view_cart, name='view_cart'),
    path('remove/<int:item_id>/',remove_from_cart, name='remove_from_cart'),
    path('checkout/<int:product_id>/', checkout, name='checkout_with_product'),
    path('checkout/', checkout, name='checkout'),
    path('place-order/',place_order, name='place_order'),
    path('my-orders/', my_orders, name='my_orders'),
]
