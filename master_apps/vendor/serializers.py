from rest_framework import serializers
from .models import Vendor


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ["id", "name", "code", "description", "is_active", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_code(self, value):
        instance = self.instance
        qs = Vendor.objects.filter(code=value)
        if instance:
            qs = qs.exclude(pk=instance.pk)
        if qs.exists():
            raise serializers.ValidationError("A vendor with this code already exists.")
        return value


class VendorNestedSerializer(serializers.ModelSerializer):
    """Returns vendor with all its mapped products (nested)."""
    products = serializers.SerializerMethodField()

    class Meta:
        model = Vendor
        fields = ["id", "name", "code", "description", "is_active", "products"]

    def get_products(self, obj):
        from master_apps.product.serializers import ProductSerializer
        mappings = obj.vendor_products.filter(is_active=True).select_related("product")
        return [
            {
                "mapping_id": m.id,
                "primary_mapping": m.primary_mapping,
                "product": ProductSerializer(m.product).data
            }
            for m in mappings
        ]
