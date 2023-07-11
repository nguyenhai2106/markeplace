'''
Created on Jun 25, 2023

@author: nguye
'''
from django.urls import path
from accounts import views

urlpatterns = [
    path('registerUser/', views.registerUser, name='registerUser')
]