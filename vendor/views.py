from django.shortcuts import render, redirect
from accounts.forms import UserForm
from vendor.forms import VendorForm
from accounts.models import User
from django.template.defaultfilters import slugify
from accounts.models import UserProfile
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from accounts.utils import send_verification_email


# Create your views here.
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
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
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
                messages.success(request, "Your restaurent has been registered successfully. Please wait for the approval.")
                # Send verification email
                send_verification_email(request, user)
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
