from django.urls import path
from .views import VendorProductMappingListCreateView, VendorProductMappingDetailView

urlpatterns = [
    path("vendor-product-mappings/", VendorProductMappingListCreateView.as_view(), name="vendor-product-mapping-list"),
    path("vendor-product-mappings/<int:pk>/", VendorProductMappingDetailView.as_view(), name="vendor-product-mapping-detail"),
]
