from django.contrib import admin
from market.models import CartItem, Tax


# Register your models here.
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'fooditem', 'quantity', 'updated_at')


class TaxAdmin(admin.ModelAdmin):
    list_display = ('tax_type', 'tax_percentage', 'is_active')


admin.site.register(CartItem, CartAdmin)
admin.site.register(Tax, TaxAdmin)
