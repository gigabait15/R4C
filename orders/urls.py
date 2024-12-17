from django.urls import path
from orders.views import OrderListView, CreateOrderView
from orders.apps import OrdersConfig

app_name = OrdersConfig.name


urlpatterns = [
    path('', OrderListView.as_view(), name='order_list'),
    path('create/', CreateOrderView.as_view(), name='order_create'),
]
