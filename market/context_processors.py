from market.models import CartItem, Tax
from menu.models import FoodItem


def get_cart_counter(request):
    cart_count = 0
    if request.user.is_authenticated:
        try:
            cart_items = CartItem.objects.filter(user=request.user)
            if cart_items:
                for cart_item in cart_items:
                    cart_count += cart_item.quantity
            else:
                cart_count = 0
        except:
            cart_count = 0
    return dict(cart_count=cart_count)


def get_cart_amounts(request):
    subtotal = 0
    tax = 0
    total = 0
    tax_dict = {}
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        for item in cart_items:
            food_item = FoodItem.objects.get(pk=item.fooditem.id)
            subtotal += (food_item.price * item.quantity)
        taxes = Tax.objects.filter(is_active=True)
        for t in taxes:
            tax_type = t.tax_type
            tax_percentage = t.tax_percentage
            tax_amount = round(tax_percentage * subtotal / 100, 2)
            tax_dict.update({tax_type: {str(tax_percentage): tax_amount}})
            tax += tax_amount

        total = subtotal + tax
    return dict(subtotal=subtotal, tax=tax, total=total, tax_dict=tax_dict)
