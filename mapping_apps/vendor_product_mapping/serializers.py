from rest_framework import serializers
from .models import VendorProductMapping


class VendorProductMappingSerializer(serializers.ModelSerializer):
    vendor_name = serializers.CharField(source="vendor.name", read_only=True)
    product_name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = VendorProductMapping
        fields = ["id", "vendor", "vendor_name", "product", "product_name",
                  "primary_mapping", "is_active", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate(self, data):
        instance = self.instance
        vendor = data.get("vendor", instance.vendor if instance else None)
        product = data.get("product", instance.product if instance else None)
        primary_mapping = data.get("primary_mapping", instance.primary_mapping if instance else False)

        # Duplicate pair check
        qs = VendorProductMapping.objects.filter(vendor=vendor, product=product)
        if instance:
            qs = qs.exclude(pk=instance.pk)
        if qs.exists():
            raise serializers.ValidationError("This vendor-product mapping already exists.")

        # Primary mapping uniqueness per vendor
        if primary_mapping:
            primary_qs = VendorProductMapping.objects.filter(vendor=vendor, primary_mapping=True)
            if instance:
                primary_qs = primary_qs.exclude(pk=instance.pk)
            if primary_qs.exists():
                raise serializers.ValidationError(
                    "This vendor already has a primary product mapping. Only one primary mapping is allowed per vendor."
                )
        return data
