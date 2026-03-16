from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Vendor


class VendorModelTest(TestCase):
    def setUp(self):
        self.vendor = Vendor.objects.create(name="Test Vendor", code="TV001", description="A test vendor")

    def test_vendor_created(self):
        self.assertEqual(Vendor.objects.count(), 1)

    def test_vendor_str(self):
        self.assertEqual(str(self.vendor), "Test Vendor (TV001)")

    def test_vendor_default_active(self):
        self.assertTrue(self.vendor.is_active)

    def test_vendor_code_unique(self):
        with self.assertRaises(Exception):
            Vendor.objects.create(name="Duplicate", code="TV001")


class VendorAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.vendor = Vendor.objects.create(name="Vendor A", code="VA001")

    def test_list_vendors(self):
        res = self.client.get("/api/vendors/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(res.data["success"])

    def test_create_vendor(self):
        res = self.client.post("/api/vendors/", {"name": "New Vendor", "code": "NV001"}, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vendor.objects.count(), 2)

    def test_create_vendor_duplicate_code(self):
        res = self.client.post("/api/vendors/", {"name": "Another", "code": "VA001"}, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_vendor_missing_name(self):
        res = self.client.post("/api/vendors/", {"code": "XX001"}, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_vendor(self):
        res = self.client.get(f"/api/vendors/{self.vendor.id}/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["data"]["code"], "VA001")

    def test_retrieve_vendor_not_found(self):
        res = self.client.get("/api/vendors/9999/")
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_vendor(self):
        res = self.client.put(f"/api/vendors/{self.vendor.id}/", {"name": "Updated", "code": "VA001"}, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["data"]["name"], "Updated")

    def test_partial_update_vendor(self):
        res = self.client.patch(f"/api/vendors/{self.vendor.id}/", {"name": "Patched"}, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_soft_delete_vendor(self):
        res = self.client.delete(f"/api/vendors/{self.vendor.id}/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.vendor.refresh_from_db()
        self.assertFalse(self.vendor.is_active)

    def test_filter_by_active(self):
        Vendor.objects.create(name="Inactive", code="INC001", is_active=False)
        res = self.client.get("/api/vendors/?is_active=true")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        for v in res.data["data"]:
            self.assertTrue(v["is_active"])
