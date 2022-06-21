from django.contrib import admin
from payment.models import Product, Review, Order, OrderItem, ShippingAddress


class ReviewAdmin(admin.ModelAdmin):
    model = Review
    list_display = ('product', 'rating', 'createdAt')


admin.site.register(Product)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
