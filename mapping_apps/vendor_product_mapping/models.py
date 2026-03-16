from django.db import models
from core.base_model import TimeStampedModel
from master_apps.vendor.models import Vendor
from master_apps.product.models import Product


class VendorProductMapping(TimeStampedModel):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="vendor_products")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_vendors")
    primary_mapping = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "vendor_product_mapping"
        unique_together = [("vendor", "product")]
        ordering = ["-created_at"]

    def __str__(self):
        return f"Vendor {self.vendor} -> Product {self.product}"
