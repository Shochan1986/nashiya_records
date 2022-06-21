from payment.urls.order_urls import order_urls
from payment.urls.product_urls import product_urls
from payment.urls.general_urls import general_urls

app_name = "payment"
urlpatterns = order_urls + product_urls + general_urls