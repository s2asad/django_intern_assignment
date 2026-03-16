from django.urls import path
from .views import VendorListCreateView, VendorDetailView, VendorNestedView

urlpatterns = [
    path("vendors/", VendorListCreateView.as_view(), name="vendor-list-create"),
    path("vendors/<int:pk>/", VendorDetailView.as_view(), name="vendor-detail"),
    path("vendors/<int:pk>/nested/", VendorNestedView.as_view(), name="vendor-nested"),
]
