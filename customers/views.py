from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from accounts.forms import UserProfileForm
from customers.forms import UserInforForm
from accounts.models import User, UserProfile
from django.contrib import messages

from orders.models import Order, OrderedFood
from django.core.exceptions import PermissionDenied


def check_role_customer(user):
    if user.role == 2:
        print("DEBUGS")
        return True
    else:
        raise PermissionDenied


# Create your views here.
@login_required(login_url='login')
@user_passes_test(check_role_customer)
def customer_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        user_form = UserInforForm(request.POST, instance=request.user)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            messages.success(request, "Đã cập nhật thông tin thành công")
            return redirect('customer_profile')
        else:
            print(profile_form.errors)
            print(user_form.errors)
    else:
        profile_form = UserProfileForm(instance=profile)
        user_form = UserInforForm(instance=request.user)
    context = {
        'profile_form': profile_form,
        'user_form': user_form,
        'profile': profile
    }
    return render(request, 'customers/customer_profile.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_customer)
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-updated_at')
    order_status = []
    for order in orders:
        if order.status not in order_status:
            order_status.append(order.status)
    context = {
        'orders': orders,
        'order_status': order_status
    }
    return render(request, 'customers/my_orders.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_customer)
def order_detail(request, order_number=None):
    order = Order.objects.get(order_number=order_number)
    ordered_foods = OrderedFood.objects.filter(order=order)
    order_subtotal = order.total - order.total_tax
    context = {
        'order': order,
        'ordered_foods': ordered_foods,
        'order_subtotal': order_subtotal
    }
    return render(request, 'customers/order_detail.html', context)
