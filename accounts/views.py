from django.shortcuts import render, redirect
from .forms import UserForm
from vendor.forms import VendorForm
from accounts.models import User
from django.contrib import messages

# Create your views here.


def registerUser(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = User.CUSTOMER
            user.save()
            messages.success(request, "Your account has been registered successfully")
            return redirect('registerUser')
        else:
            print("DEBUGS:", form.errors)
    else:
        form = UserForm()
    context = {
        'form':form,
    }
    return render(request, 'accounts/registerUser.html', context)


def registerVendor(request):
    user_form = UserForm()
    vendor_form = VendorForm()
    if user_form.is_valid() and vendor_form.is_valid():
        first_name = user_form.cleaned_data['first_name']
    context = {
        'user_form': user_form,
        'vendor_form': vendor_form
    }
    
    return render(request, 'accounts/registerVendor.html', context)

