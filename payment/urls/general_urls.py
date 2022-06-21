from django.urls import path
from payment.views import general_views as views


general_urls = [
    path('test/', views.test_payment, name='test-payment'),
    path('save-stripe-info/', views.save_stripe_info, name='save-stripe-info'),

]