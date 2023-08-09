from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Prefetch, Q

from market.context_processors import get_cart_counter, get_cart_amounts
from vendor.models import Vendor
from menu.models import Category, FoodItem
from market.models import CartItem


# Create your views here.
def market(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    vendor_count = vendors.count()
    context = {
        'vendors': vendors,
        'vendor_count': vendor_count
    }
    return render(request, 'market/listings.html', context)


def vendor_detail(request, vendor_slug, category_slug=None):
    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)
    if category_slug != 'all':
        categories = Category.objects.filter(vendor=vendor, slug=category_slug).prefetch_related(
            Prefetch(
                'fooditems',
                queryset=FoodItem.objects.filter(is_available=True)
            )
        )
    else:
        categories = Category.objects.filter(vendor=vendor).prefetch_related(
            Prefetch(
                'fooditems',
                queryset=FoodItem.objects.filter(is_available=True)
            )
        )
    category_list = Category.objects.filter(vendor=vendor)
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        cart_items = None
    context = {
        'vendor': vendor,
        'categories': categories,
        'category_list': category_list,
        'cart_items': cart_items
    }
    return render(request, 'market/vendor_detail.html', context)


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def add_to_cart(request, food_id=None):
    if request.user.is_authenticated:
        if is_ajax(request):
            try:
                food_item = FoodItem.objects.get(id=food_id)
                try:
                    cart_item_existed = CartItem.objects.get(user=request.user, fooditem=food_item)
                    cart_item_existed.quantity += 1
                    cart_item_existed.save()
                    return JsonResponse({
                        'status': 'Success',
                        'message': f"Đã cập nhật số lượng sản phẩm '{cart_item_existed.fooditem.food_title}'",
                        'cart_counter': get_cart_counter(request),
                        'quantity': cart_item_existed.quantity,
                        'subtotal_of_item': cart_item_existed.quantity * cart_item_existed.fooditem.price,
                        'cart_amounts': get_cart_amounts(request)
                    })
                except:
                    new_cart = CartItem.objects.create(user=request.user, fooditem=food_item, quantity=1)
                    return JsonResponse({
                        'status': 'Success',
                        'message': f"Đã thêm sản phẩm '{new_cart.fooditem.food_title}' vào giỏ hàng",
                        'cart_counter': get_cart_counter(request),
                        'quantity': new_cart.quantity,
                        'subtotal_of_item': new_cart.fooditem.price,
                        'cart_amounts': get_cart_amounts(request)

                    })
            except:
                return JsonResponse({
                    'status': 'Failed',
                    'message': "Không tìm thấy món ăn đã yêu cầu!"
                })
        else:
            return JsonResponse({
                'status': 'Failed',
                'message': "Yêu cầu không hợp lệ!"
            })
    else:
        return JsonResponse({
            'status': 'login_required',
            'message': "Vui lòng đăng nhập để tiếp tục đặt hàng!"
        })


def decrease_cart(request, food_id):
    if request.user.is_authenticated:
        if is_ajax(request):
            try:
                food_item = FoodItem.objects.get(id=food_id)
                try:
                    cart_item_existed = CartItem.objects.get(user=request.user, fooditem=food_item)
                    if cart_item_existed.quantity > 1:
                        cart_item_existed.quantity -= 1
                        cart_item_existed.save()
                    else:
                        cart_item_existed.delete()
                        cart_item_existed.quantity = 0
                    return JsonResponse({
                        'status': 'Success',
                        'message': f"Đã cập nhật số lượng sản phẩm '{cart_item_existed.fooditem.food_title}'",
                        'cart_counter': get_cart_counter(request),
                        'quantity': cart_item_existed.quantity,
                        'subtotal_of_item': cart_item_existed.quantity * cart_item_existed.fooditem.price,
                        'food_name': food_item.food_title,
                        'cart_amounts': get_cart_amounts(request)
                    })
                except:
                    return JsonResponse({
                        'status': 'Failed',
                        'message': 'Không tìm thấy món ăn này trong giỏ hàng!',
                    })
            except:
                return JsonResponse({
                    'status': 'Failed',
                    'message': "Không tìm thấy món ăn đã yêu cầu!",
                })
        else:
            return JsonResponse({
                'status': 'Failed',
                'message': "Yêu cầu không hợp lệ!"
            })
    else:
        return JsonResponse({
            'status': 'login_required',
            'message': "Vui lòng đăng nhập để tiếp tục đặt hàng!"
        })


@login_required(login_url='login')
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user).order_by('created_at')
    context = {
        'cart_items': cart_items,
    }
    return render(request, 'market/cart.html', context)


@login_required(login_url='login')
def delete_cart_item(request, cart_item_id):
    if request.user.is_authenticated:
        if is_ajax(request):
            try:
                cart_item = CartItem.objects.get(user=request.user, id=cart_item_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({
                        'status': 'Success',
                        'message': f"Món ăn {cart_item.fooditem.food_title} đã được xóa khỏi giỏ hàng!",
                        'cart_counter': get_cart_counter(request),
                        'cart_amounts': get_cart_amounts(request),
                    })
            except:
                return JsonResponse({
                    'status': 'Failed',
                    'message': 'Không tìm thấy món ăn này trong giỏ hàng!',
                })
        else:
            return JsonResponse({
                'status': 'Failed',
                'message': "Yêu cầu không hợp lệ!"
            })


def search(request):
    keyword = request.GET['restaurant_name']
    fetch_vendors_by_fooditems = FoodItem.objects.filter(food_title__icontains=keyword, is_available=True).values_list(
        'vendor', flat=True)

    vendors = Vendor.objects.filter(Q(id__in=fetch_vendors_by_fooditems) | Q(is_approved=True, user__is_active=True,
                                                                             vendor_name__icontains=keyword))
    vendor_count = vendors.count()
    context = {
        'vendors': vendors,
        'vendor_count': vendor_count
    }
    return render(request, 'market/listings.html', context)
