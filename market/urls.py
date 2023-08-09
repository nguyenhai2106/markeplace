from django.urls import path
from market import views

urlpatterns = [
    path('', views.market, name='market'),
    path('add_to_cart/<int:food_id>/', views.add_to_cart, name='add_to_cart'),
    path('decrease_cart/<int:food_id>/', views.decrease_cart, name='decrease_cart'),
    path('delete_cart_item/<int:cart_item_id>/', views.delete_cart_item, name='delete_cart_item'),
    path('cart/', views.cart, name='cart'),
    path('search', views.search, name='search'),
    path('<slug:vendor_slug>/<slug:category_slug>/', views.vendor_detail, name='vendor_detail'),
]
