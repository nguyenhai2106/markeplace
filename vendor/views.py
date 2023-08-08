from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import IntegrityError
from django.http import QueryDict
from django.shortcuts import render, redirect, get_object_or_404
from accounts.forms import UserForm, UserProfileForm
from accounts.views import check_role_vendor
from vendor.forms import VendorForm, Vendor
from accounts.models import User
from django.template.defaultfilters import slugify
from accounts.models import UserProfile
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from accounts.utils import send_verification_email
from menu.models import Category, FoodItem
from menu.forms import CategoryForm, FoodItemForm


# Create your views here.
def get_vendor(request):
    vendor = Vendor.objects.get(user=request.user)
    return vendor


def registerVendor(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect("dashboard")
    elif request.method == 'POST':
        user_form = UserForm(request.POST)
        vendor_form = VendorForm(request.POST, request.FILES)
        if user_form.is_valid() and vendor_form.is_valid():
            first_name = user_form.cleaned_data['first_name']
            last_name = user_form.cleaned_data['last_name']
            username = user_form.cleaned_data['username']
            email = user_form.cleaned_data['email']
            password = user_form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email,
                                            password=password)
            user.role = User.VENDOR
            user.save()
            vendor = vendor_form.save(commit=False)
            vendor.user = user
            vendor_name = vendor_form.cleaned_data['vendor_name']
            vendor_slug = slugify(vendor_name) + '-' + str(user.id)
            vendor.vendor_slug = vendor_slug
            try:
                user_profile = UserProfile.objects.get(user=user)
                vendor.user_profile = user_profile
                vendor.save()
                messages.success(request,
                                 "Your restaurant has been registered successfully. Please wait for the approval.")
                # Send verification email
                mail_subject = 'Please active your account'
                email_template = 'accounts/emails/account_verification_email.html'
                send_verification_email(request, user, mail_subject, email_template)
                return redirect("login")
            except ObjectDoesNotExist:
                messages.error(request, "UserProfile not found for the user.")
        else:
            error_list = ""
            if user_form.errors:
                print("DEBUGS:", user_form.errors)
                for error_messages in user_form.errors.values():
                    for error_message in error_messages:
                        error_list += error_message + " "
                    break
            else:
                print("DEBUGS:", vendor_form.errors)
                for error_messages in vendor_form.errors.values():
                    for error_message in error_messages:
                        error_list += error_message + " "
                    break
            messages.error(request, error_list)
    else:
        user_form = UserForm()
        vendor_form = VendorForm()
    user_form = UserForm()
    vendor_form = VendorForm()
    context = {
        'user_form': user_form,
        'vendor_form': vendor_form
    }

    return render(request, 'accounts/registerVendor.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendor_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, 'Các thông tin đã được cập nhật')
            return redirect('vendorProfile')
        else:
            print(profile_form.errors)
            print(vendor_form.errors)
    else:
        profile_form = UserProfileForm(instance=profile)
        vendor_form = VendorForm(instance=vendor)
    context = {
        'profile_form': profile_form,
        'vendor_form': vendor_form,
        'profile': profile,
        'vendor': vendor
    }

    return render(request, 'vendor/vendor_profile.html', context)


def menu_builder(request):
    vendor = get_vendor(request)
    categories = Category.objects.filter(vendor=vendor).order_by('created_at')
    context = {
        'categories': categories
    }
    return render(request, 'vendor/menu_builder.html', context)


def food_items_by_category(request, pk=None):
    vendor = get_vendor(request)
    category = get_object_or_404(Category, pk=pk)
    food_items = FoodItem.objects.filter(vendor=vendor, category=category)
    context = {
        'food_items': food_items,
        'category': category
    }
    return render(request, 'vendor/food_items_by_category.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            try:
                category = form.save(commit=False)
                category.vendor = get_vendor(request)
                category.save()
                messages.success(request, "Thêm danh mục thành công")
                return redirect('menu_builder')
            except IntegrityError as e:
                print("DEBUGS")
                messages.error(request, "Danh mục này đã tồn tại!")
                return redirect('add_category')
        else:
            print("DEBUGS:", form.errors)
    else:
        form = CategoryForm()
    context = {
        'form': form
    }
    return render(request, 'vendor/add_category.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.save()
            messages.success(request, "Cập nhật danh mục thành công")
            return redirect('menu_builder')
        else:
            print("DEBUGS:", form.errors)
    else:
        form = CategoryForm(instance=category)
    context = {
        'form': form,
        'category': category
    }
    return render(request, 'vendor/edit_category.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.warning(request, f"Danh mục '{category}' đã bị xóa")
    return redirect('menu_builder')


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_food(request):
    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES)
        if form.is_valid():
            food_item = form.save(commit=False)
            food_item.vendor = get_vendor(request)
            food_item.save()
            messages.success(request, "Thêm món ăn thành công")
            return redirect('food_items_by_category', food_item.category.id)
        else:
            print("DEBUGS:", form.errors)
    else:
        form = FoodItemForm()
        form.fields['category'].queryset = Category.objects.filter(vendor=get_vendor(request))
    context = {
        'form': form
    }
    return render(request, 'vendor/add_food.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_food(request, pk=None):
    food_item = get_object_or_404(FoodItem, pk=pk)
    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES, instance=food_item)
        if form.is_valid():
            food_item = form.save(commit=False)
            food_item.vendor = get_vendor(request)
            form.save()
            messages.success(request, "Cập nhật món ăn thành công")
            return redirect('food_items_by_category', food_item.category.id)
        else:
            print("DEBUGS:", form.errors)
    else:
        form = FoodItemForm(instance=food_item)
        form.fields['category'].queryset = Category.objects.filter(vendor=get_vendor(request))
    context = {
        'form': form,
        'food_item': food_item
    }
    return render(request, 'vendor/edit_food.html', context)


def delete_food(request, pk=None):
    food_item = get_object_or_404(FoodItem, pk=pk)
    food_item.delete()
    messages.warning(request, f"Món ăn '{food_item.food_title}' đã bị xóa")
    return redirect('food_items_by_category', food_item.category.id)
