from django.urls import path
from payment.views import order_views as views


order_urls = [

    path('orders/', views.getOrders, name='orders'),
    path('orders/add/', views.addOrderItems, name='orders-add'),
    path('orders/myorders/', views.getMyOrders, name='myorders'),

    path('orders/<str:pk>/deliver/', views.updateOrderToDelivered, name='order-delivered'),

    path('orders/<str:pk>/', views.getOrderById, name='user-order'),
    path('orders/<str:pk>/pay/', views.updateOrderToPaid, name='pay'),
]