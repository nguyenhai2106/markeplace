'''
Created on Jun 25, 2023

@author: nguye
'''
from django.urls import path
from accounts import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('registerUser/', views.registerUser, name='registerUser'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('myAccount', views.myAccount, name='myAccount'),
    path('custDashboard/', views.custDashboard, name='custDashboard'),
    path('vendorDashboard/', views.vendorDashboard, name='vendorDashboard'),
    
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('request_password_validate/<uidb64>/<token>', views.request_password_validate, name='request_password_validate'),
    path('reset_password/', views.reset_password, name='reset_password'),
]