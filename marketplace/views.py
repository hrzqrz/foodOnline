from django.shortcuts import render, redirect, get_object_or_404
from vendor.models import Vendor, OpeningHour
from menu.models import Category, FoodItem
from django.db.models import Prefetch
from django.http import HttpResponse, JsonResponse
from marketplace.models import Cart
from marketplace.context_processor import get_cart_counter, get_cart_amounts
from django.contrib.auth.decorators import login_required
from django.db.models import Q 
from datetime import date, datetime
from orders.forms import OrderForm
from accounts.models import UserProfile
# Create your views here.

def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    vendors_count = vendors.count()
    context = {
        'vendors': vendors,
        'vendors_count': vendors_count
    }
    return render(request, 'marketplace/listings.html', context)

def vendor_detail(request, vendor_slug):
    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)
    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'fooditem',
            queryset=FoodItem.objects.filter(is_available=True)
        )
    )
    
    opening_hours = OpeningHour.objects.filter(vendor=vendor).order_by('day', '-from_hour')
    #Check current day is opening hours
    today_date = date.today()
    today = today_date.isoweekday()
    current_day_opening_hours = OpeningHour.objects.filter(vendor=vendor, day=today)
    
           
    
    # print(opening_hours)
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None
    context = {
        'vendor': vendor,
        'categories': categories,
        'cart_items': cart_items,
        'opening_hours': opening_hours,
        'current_day_opening_hours': current_day_opening_hours,
    }
    return render(request, 'marketplace/vendor_detail.html', context)


def add_to_cart(request, food_id):
    # return HttpResponse('testing')
    if request.user.is_authenticated:
        # if request.is_ajax():
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            #Check if the food item exists
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                # Check if the user has already added food to the cart
                try:
                    chkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    # Increase the cart quantity
                    chkCart.quantity += 1
                    chkCart.save()
                    return JsonResponse({'status': 'Success',
                                         'message': 'Increased the cart quantity.',
                                         'cart_counter': get_cart_counter(request),
                                         'qty': chkCart.quantity,
                                         'cart_amount': get_cart_amounts(request)})
                except:
                    chkCart = Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)
                    return JsonResponse({'status': 'Success',
                                         'message': 'Added the food to the cart',
                                         'cart_counter': get_cart_counter(request),
                                         'qty': chkCart.quantity,
                                         'cart_amount': get_cart_amounts(request)})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'This food does not exist!' })
        else:
             return JsonResponse({'status': 'Failed', 'message': 'Invalid request'})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'please login to cintinue'})
   
   
 
def decrease_cart(request, food_id):
    if request.user.is_authenticated:
        # if request.is_ajax():
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            #Check if the food item exists
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                # Check if the user has already added food to the cart
                try:
                    chkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    # decrease the cart quantity
                    if chkCart.quantity > 1:
                        chkCart.quantity -= 1
                        chkCart.save()
                    else:
                        chkCart.delete()
                        chkCart.quantity = 0
                    return JsonResponse({'status': 'Success', 'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity, 'cart_amount': get_cart_amounts(request)})
                except:
                    return JsonResponse({'status': 'Success', 'message': 'You dont have this item in your cart.', 'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity, 'cart_amount': get_cart_amounts(request)})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'This food does not exist!' })
        else:
             return JsonResponse({'status': 'Failed', 'message': 'Invalid request'})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'please login to cintinue'})
    
@login_required(login_url='login')   
def cart(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    context = {
        'cart_items': cart_items,
    }
    return render(request, 'marketplace/cart.html', context)

def delete_cart(request, cart_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                # Check if the cart item exists
                cart_item = Cart.objects.get(user=request.user, id=cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({'status': 'Success', 'message': 'Cart item has been deleted!', 'cart_counter': get_cart_counter(request), 'cart_amount': get_cart_amounts(request)})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'Cart item does not exist!'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})
        
def search(request):
    address = request.GET['address']
    latitude = request.GET['lat']
    longitude = request.GET['lng']
    radius = request.GET['radius']
    keyword = request.GET['keyword']
    
    # get vendor ids that has the food item the user is looking for
    fetch_vendors_by_fooditems = FoodItem.objects.filter(food_title__icontains=keyword, is_available=True).values_list('vendor', flat=True)
    # print(fetch_vendors_by_fooditems)
    vendors = Vendor.objects.filter(Q(id__in=fetch_vendors_by_fooditems) | Q(vendor_name__icontains=keyword, is_approved=True, user__is_active=True))
    # vendors = Vendor.objects.filter()
    vendor_count = vendors.count()
    # print(vendors)
    context = {
        'vendors': vendors,
        'vendors_count': vendor_count,
    }
    return render(request, 'marketplace/listings.html', context)
@login_required(login_url='login')
def checkout(request):
    user_profile = UserProfile.objects.get(user=request.user)
    default_values = {
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'phone': request.user.phone_number,
        'email': request.user.email,
        'address': user_profile.address,
        'country': user_profile.country,
        'state': user_profile.state,
        'city': user_profile.city,
        'pin_conde': user_profile.pin_code,
    }
    form = OrderForm(initial=default_values)
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('marketplace')
    context = {
        'form': form,
        'cart_items': cart_items,
    }
    return render(request, 'marketplace/checkout.html', context)