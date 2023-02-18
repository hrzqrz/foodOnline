from django.contrib import admin
from .models import Payment, Order, OrderedFood
# Register your models here.
class OrderedFoodInLine(admin.TabularInline):
    model = OrderedFood
    readonly_fields = ('order', 'payment', 'user', 'fooditem', 'quantity', 'price', 'amount')
    extra = 0
    
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'name', 'phone', 'email', 'total', 'payment_method', 'status', 'order_place_to', 'is_ordered']
    inlines = [OrderedFoodInLine]

admin.site.register(Payment)
admin.site.register(Order)
admin.site.register(OrderedFood)
