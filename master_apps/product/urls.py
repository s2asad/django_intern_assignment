from django.urls import path
from .views import ProductListCreateView, ProductDetailView, ProductNestedView

urlpatterns = [
    path("products/", ProductListCreateView.as_view(), name="product-list-create"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
    path("products/<int:pk>/nested/", ProductNestedView.as_view(), name="product-nested"),
]
