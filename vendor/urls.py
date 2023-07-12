from django.urls import path
from vendor import views

urlpatterns = [
    path('registerVendor/', views.registerVendor, name='registerVendor')
]
