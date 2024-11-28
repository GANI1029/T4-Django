from django.urls import path
from . import views

urlpatterns = [
    path('inventory/items/', views.inventory_items),
    path('inventory/items/<int:pk>/', views.inventory_item_detail),
    path('items/sort/', views.inventory_items_sort),
    path('items/query/<str:category>/', views.inventory_items_query_category),
]
