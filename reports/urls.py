from django.urls import path
from  reports import views

urlpatterns = [
    path('revenue_report/', views.revenue_report, name="revenue_report"),
]
