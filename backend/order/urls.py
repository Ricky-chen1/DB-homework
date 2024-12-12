from django.urls import path
from .views import create_order_view, order_list_view, order_detail_view
from .views import pay_order_view, cancel_order_view

urlpatterns = [
    path('buy', create_order_view, name='create-order'),
    path('list', order_list_view, name='order-list'),
    path('<int:order_id>', order_detail_view, name='order-detail'),
    path('pay', pay_order_view, name='pay_order'),
    path('cancel', cancel_order_view, name='cancel_order'),
]
