from django.contrib import admin
from market.models import CartItem


# Register your models here.
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'fooditem', 'quantity', 'updated_at']


admin.site.register(CartItem, CartAdmin)
