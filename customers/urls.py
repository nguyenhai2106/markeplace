from django.urls import path
from accounts import views as account_view
from customers import views

urlpatterns = [
    path('', account_view.custDashboard, name='customer'),
    path('profile/', views.customer_profile, name='customer_profile')
]
