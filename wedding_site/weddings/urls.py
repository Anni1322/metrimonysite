from django.urls import path
from . import views

urlpatterns = [
    path('planner/', views.wedding_planner, name='wedding_planner'),
    path('unbooked/', views.unbooked_weddings, name='unbooked_weddings'),
    path('vendors/', views.vendor_search, name='vendor_search'),
]