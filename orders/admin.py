from django.contrib import admin
from orders.models import Payment, Order, OrderedFood


class OrderedFoodInline(admin.TabularInline):
    model = OrderedFood
    readonly_fields = ('order', 'payment', 'user', 'food_item', 'quantity', 'price', 'amount')
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'customer_name', 'phone_number', 'email', 'total', 'payment_method', 'status',
                    'order_placed_to', 'is_ordered']
    inlines = [OrderedFoodInline]


# Register your models here.
admin.site.register(Payment)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderedFood)
