import simplejson as json
from django.http import JsonResponse

from django.shortcuts import render, HttpResponse, redirect

from market.models import CartItem
from django.contrib import messages
from market.context_processors import get_cart_amounts
from orders.forms import OrderForm
from orders.models import Order, Payment, OrderedFood
from orders.utils import generate_order_number
from accounts.utils import send_notification_email
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='login')
def place_order(request):
    cart_items = CartItem.objects.filter(user=request.user).order_by('created_at')
    cart_count = cart_items.count()
    if cart_count <= 0:
        messages.warning(request, "Giỏ hàng của bạn chưa có sản phẩm!")
        return redirect('cart')
    subtotal = get_cart_amounts(request)['subtotal']
    total_tax = get_cart_amounts(request)['tax']
    total = get_cart_amounts(request)['total']
    tax_data = get_cart_amounts(request)['tax_dict']

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order()
            order.first_name = form.cleaned_data['first_name']
            order.last_name = form.cleaned_data['last_name']
            order.phone_number = form.cleaned_data['phone_number']
            order.email = form.cleaned_data['email']
            order.address = form.cleaned_data['address']
            order.country = form.cleaned_data['country']
            order.state = form.cleaned_data['state']
            order.city = form.cleaned_data['city']
            order.pin_code = form.cleaned_data['pin_code']
            order.payment_method = request.POST['payment_method']
            order.user = request.user
            order.total = total
            order.tax_data = json.dumps(tax_data)
            order.total_tax = total_tax
            order.save()
            order.order_number = generate_order_number(order.id)
            order.save()
            context = {
                'order': order
            }
            return render(request, 'orders/place_order.html', context)
        else:
            print(form.errors)

    return render(request, 'orders/place_order.html')


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


@login_required(login_url='login')
def payment(request):
    if is_ajax(request) and request.method == 'POST':
        # Lưu thông tin thanh toán vào model Payment
        order_number = request.POST.get('order_number')
        transaction_id = request.POST.get('transaction_id')
        status = request.POST.get('status')
        payment_method = request.POST.get('payment_method')
        amount = request.POST.get('amount')
        user = request.user
        order = Order.objects.get(user=user, order_number=order_number)
        new_payment = Payment(
            user=user,
            transaction_id=transaction_id,
            payment_method=payment_method,
            amount=amount,
            status=status,
        )
        new_payment.save()
        # Cập nhật Order
        order.payment = new_payment
        order.is_ordered = True
        order.save()
        # Lưu thông tin cart item đã đặt
        cart_items = CartItem.objects.filter(user=user)
        for cart_item in cart_items:
            ordered_food = OrderedFood()
            ordered_food.order = order
            ordered_food.payment = new_payment
            ordered_food.user = cart_item.user
            ordered_food.food_item = cart_item.fooditem
            ordered_food.quantity = cart_item.quantity
            ordered_food.price = cart_item.fooditem.price
            ordered_food.amount = cart_item.fooditem.price * cart_item.quantity
            ordered_food.save()
        # Gửi email xác nhận cho khách hàng
        mail_subject = 'Đơn hàng của bạn đã được xác nhận - Cảm ơn bạn!'
        mail_template = 'orders/order_confirmation_email.html'
        context = {
            'user': user,
            'order': order,
            'to_email': order.email
        }
        send_notification_email(mail_subject, mail_template, context)

        # Gửi email cho nhà hàng
        mail_subject = 'Bạn nhận được 1 đơn hàng!'
        mail_template = 'orders/new_order_received.html'
        to_emails = []
        for cart_item in cart_items:
            if cart_item.fooditem.vendor.user.email not in to_emails:
                to_emails.append(cart_item.fooditem.vendor.user.email)
        context = {
            'order': order,
            'to_email': to_emails
        }
        send_notification_email(mail_subject, mail_template, context)
        # Xóa giỏ hàng
        cart_items.delete()
        # Trả kết quả cho request
        response = {
            'order_number': order_number,
            'transaction_id': transaction_id,
        }
        return JsonResponse(response)
    return HttpResponse("Payment Views")


def order_completed(request):
    order_number = request.GET.get('order_number')
    transaction_id = request.GET.get('transaction_id')
    print(order_number, transaction_id)
    try:
        order = Order.objects.get(order_number=order_number, payment__transaction_id=transaction_id, is_ordered=True)
        ordered_foods = OrderedFood.objects.filter(order=order)
        subtotal = 0
        for ordered_food in ordered_foods:
            subtotal += ordered_food.amount
        context = {
            'order': order,
            'ordered_foods': ordered_foods,
            'subtotal': subtotal
        }
        return render(request, 'orders/order_completed.html', context)
    except Exception as e:
        print(e)
        return redirect('home')
