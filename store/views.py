from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
import random
from store.models import *
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.core.paginator import Paginator
from django.http import HttpResponseNotFound #this is for responce not found/404 error(page not found)

User = get_user_model()
# Create your views here.
def custom_404_view(request, exception):
    return render(request, '404.html', status=404)

def home(request):
    if request.user.is_authenticated:
        return render(request,"store/home.html",context={"message":"pass"})
    else:
        return render(request,"store/home.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')  # Redirect to home if successful
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'store/login.html')

def register_view(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        profile_picture = request.FILES.get('profile_picture')  # Get the uploaded image
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, "Account created! Please login.")
            UserProfile.objects.create(user=user, profile_picture=profile_picture)
            return redirect('login')
    return render(request, 'store/register.html')

def logout_view(request):
    logout(request)
    request.session.flush()  # Clears all session data instantly
    return redirect('home')  # Redirect to login page immediately

def product_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
    message = request.GET.get('msg')
    if message:
        products = Product1.objects.filter(category = message).order_by('-id') or Product1.objects.filter(name = message).order_by('-id')
    else:
        products = Product1.objects.all().order_by('-id')
    paginator = Paginator(products, 3)  # Show 3 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'store/product_list.html', {'products': products, 'page_obj': page_obj})
   

def product_detail(request, product_id):
    # Fetch the product using the product_id
    product = get_object_or_404(Product1, id=product_id)
    
    # Render the template with the product details
    return render(request, 'store/product_detail.html', {'product': product})

    #profile view
def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)
    return render(request, 'store/profile.html', {'profile': profile})

def add_to_cart(request, product_id):
    if request.user.is_authenticated:
        product = Product1.objects.get(id=product_id)
        cart_item, created = CartItem.objects.get_or_create(product=product,user=request.user)
        cart_item.quantity += 1
        cart_item.save()
        return redirect('product_list')
    else:
        return redirect('login')

def view_cart(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        return render(request, 'store/cart.html', {'cart_items': cart_items, 'total_price': total_price,})
    else:
        return redirect('login')
    
def remove_from_cart(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    cart_item.delete()
    return redirect('view_cart')

def checkout(request,product_id=None):
    if request.user.is_authenticated:
        if product_id:
            product = get_object_or_404(Product1, id=product_id)
            cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
            if created:
                cart_item.quantity = 1 
            else:
                cart_item.quantity += 1
            cart_item.save()
        cart_items = CartItem.objects.filter(user=request.user)
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        return render(request, 'store/checkout.html', {'cart_items': cart_items, 'total_price': total_price})
    else:
        return redirect('login')

def cart_count(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        total_items = sum(item.quantity for item in cart_items)  # Sum of all quantities
    else:
        total_items = 0  # If user is not logged in

    return {'cart_count': total_items}  # Send count to all templates

def place_order(request): # this is for succeccfully orderd products
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        if not cart_items.exists():
            return redirect('checkout')

        total = sum(item.product.price * item.quantity for item in cart_items)
        order = Order.objects.create(user=request.user, total_price=total)

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        # Clear the cart
        cart_items.delete()

        return render(request, 'store/order_success.html', {'order': order})
    else:
        return redirect('login')

def my_orders(request): #this is for seen your orders 
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
        return render(request, 'store/my_orders.html', {'orders': orders})
    else:
        return redirect('login')