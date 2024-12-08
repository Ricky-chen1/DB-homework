from django.urls import path
from .views import create_order_view, order_list_view, order_detail_view

urlpatterns = [
    path('create', create_order_view, name='create-order'),
    path('list', order_list_view, name='order-list'),
    path('<int:order_id>', order_detail_view, name='order-detail'),
]
