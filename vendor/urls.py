from django.urls import path, include
from vendor import views
from accounts import views as AccountViews

urlpatterns = [
    path('', AccountViews.vendorDashboard, name='vendor'),
    path('registerVendor/', views.registerVendor, name='registerVendor'),
    path('profile/', views.vendor_profile, name='vendorProfile'),
]
