from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from master_apps.vendor.models import Vendor
from master_apps.product.models import Product
from .models import VendorProductMapping


class VendorProductMappingTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.vendor = Vendor.objects.create(name="Vendor A", code="VA001")
        self.vendor2 = Vendor.objects.create(name="Vendor B", code="VB001")
        self.product = Product.objects.create(name="Product A", code="PA001")
        self.product2 = Product.objects.create(name="Product B", code="PB001")

    def test_create_mapping(self):
        res = self.client.post("/api/vendor-product-mappings/", {
            "vendor": self.vendor.id,
            "product": self.product.id,
            "primary_mapping": True
        }, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_duplicate_mapping_rejected(self):
        VendorProductMapping.objects.create(vendor=self.vendor, product=self.product)
        res = self.client.post("/api/vendor-product-mappings/", {
            "vendor": self.vendor.id,
            "product": self.product.id,
        }, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_only_one_primary_per_vendor(self):
        VendorProductMapping.objects.create(vendor=self.vendor, product=self.product, primary_mapping=True)
        res = self.client.post("/api/vendor-product-mappings/", {
            "vendor": self.vendor.id,
            "product": self.product2.id,
            "primary_mapping": True
        }, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_second_primary_allowed_for_different_vendor(self):
        VendorProductMapping.objects.create(vendor=self.vendor, product=self.product, primary_mapping=True)
        res = self.client.post("/api/vendor-product-mappings/", {
            "vendor": self.vendor2.id,
            "product": self.product2.id,
            "primary_mapping": True
        }, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_filter_by_vendor_id(self):
        VendorProductMapping.objects.create(vendor=self.vendor, product=self.product)
        res = self.client.get(f"/api/vendor-product-mappings/?vendor_id={self.vendor.id}")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        for m in res.data["data"]:
            self.assertEqual(m["vendor"], self.vendor.id)

    def test_soft_delete_mapping(self):
        mapping = VendorProductMapping.objects.create(vendor=self.vendor, product=self.product)
        res = self.client.delete(f"/api/vendor-product-mappings/{mapping.id}/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        mapping.refresh_from_db()
        self.assertFalse(mapping.is_active)
