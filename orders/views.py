from django.shortcuts import render, redirect
from marketplace.models import Cart
from marketplace.context_processor import get_cart_amounts
from .forms import OrderForm
from .models import Order
import simplejson as json
from .utils import generate_order_number
from orders.models import FoodItem 
from marketplace.models import Tax
# Create your views here.

def place_order(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('marketplace')
    
    vendors_id = []
    for i in cart_items:
        if i.fooditem.vendor.id not in vendors_id:
            vendors_id.append(i.fooditem.vendor.id)
    
    # {"vendor_id": {"subtotal": {"tax_type": {"tax_percentage": "tax_amount"}}}}
    get_tax = Tax.objects.filter(is_active=True)
    subtotal = 0  
    k = {}   
    total_data = {}
    for i in cart_items:
        fooditem = FoodItem.objects.get(pk=i.fooditem.id, vendor_id__in=vendors_id)
        v_id = fooditem.vendor.id
        if v_id in k:
            subtotal = k[v_id]
            subtotal += (fooditem.price * i.quantity)
            k[v_id] = subtotal
        else: 
            subtotal = (fooditem.price * i.quantity)
            k[v_id] = subtotal

        #calculate the dax data
        tax_dict = {}
        for i in get_tax:
            tax_type = i.tax_type
            tax_percentage = i.tax_percentage
            tax_amount = round((tax_percentage * subtotal) / 100, 2)
            tax_dict.update({tax_type: {str(tax_percentage): str(tax_amount)}})
        #construct total_data
        total_data.update({fooditem.vendor.id: {str(subtotal): str(tax_dict)}})
    
        
    subtotal = get_cart_amounts(request)['subtotal']
    total_tax = get_cart_amounts(request)['tax']
    grand_total = get_cart_amounts(request)['grand_total']
    tax_data = get_cart_amounts(request)['tax_dict']
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order()
            order.first_name = form.cleaned_data['first_name']
            order.last_name = form.cleaned_data['last_name']
            order.phone = form.cleaned_data['phone']
            order.email = form.cleaned_data['email']
            order.address = form.cleaned_data['address']
            order.country = form.cleaned_data['country']
            order.city = form.cleaned_data['city']
            order.state = form.cleaned_data['state']
            order.pin_code = form.cleaned_data['pin_code']
            order.user = request.user
            order.total = grand_total
            order.tax_data = json.dumps(tax_data)
            order.total_data = json.dumps(total_data)
            order.total_tax = total_tax
            order.payment_method = request.POST['payment_method']
            order.save() #order id or pk is generated
            order.order_number = generate_order_number(order.id)
            order.vendors.add(*vendors_id)
            order.save()
            return redirect('place_order')
        else:
            print(form.errors)
    return render(request, 'orders/place_order.html')
