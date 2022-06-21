from django.urls import path
from payment.views import product_views as views

product_urls = [
    path('products/', views.getProducts, name="products"),
    path('products/all/', views.getAllProducts, name="products-all"),

    path('products/create/', views.createProduct, name="product-create"),
    path('products/upload/', views.uploadImage, name="image-upload"),

    path('products/<str:pk>/reviews/', views.createProductReview, name="create-review"),
    path('products/top/', views.getTopProducts, name='top-products'),
    path('products/<str:pk>/', views.getProduct, name="product"),

    path('products/update/<str:pk>/', views.updateProduct, name="product-update"),
    path('products/delete/<str:pk>/', views.deleteProduct, name="product-delete"),
]