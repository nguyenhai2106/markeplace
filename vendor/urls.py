from django.urls import path, include
from vendor import views
from accounts import views as AccountViews

urlpatterns = [
    path('', AccountViews.vendorDashboard, name='vendor'),
    path('registerVendor/', views.registerVendor, name='registerVendor'),
    path('profile/', views.vendor_profile, name='vendorProfile'),
    path('menu-builder/', views.menu_builder, name='menu_builder'),
    path('menu-builder/category/<int:pk>/', views.food_items_by_category, name='food_items_by_category'),

    # Category
    path('menu-builder/category/add', views.add_category, name="add_category"),
    path('menu-builder/category/edit/<int:pk>/', views.edit_category, name="edit_category"),
    path('menu-builder/category/delete/<int:pk>/', views.delete_category, name="delete_category"),

    # FoodItem
    path('menu-builder/food/add', views.add_food, name="add_food"),
    path('menu-builder/food/edit/<int:pk>/', views.edit_food, name="edit_food"),
    path('menu-builder/food/delete/<int:pk>/', views.delete_food, name="delete_food"),
    path('order_detail/<int:order_number>', views.order_detail, name='vendor_order_detail'),
    path('my_orders/', views.my_orders, name='vendor_my_orders'),
]
