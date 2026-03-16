from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "code", "description", "is_active", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_code(self, value):
        instance = self.instance
        qs = Product.objects.filter(code=value)
        if instance:
            qs = qs.exclude(pk=instance.pk)
        if qs.exists():
            raise serializers.ValidationError("A product with this code already exists.")
        return value


class ProductNestedSerializer(serializers.ModelSerializer):
    """Returns product with all its mapped courses (nested)."""
    courses = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ["id", "name", "code", "description", "is_active", "courses"]

    def get_courses(self, obj):
        from master_apps.course.serializers import CourseSerializer
        mappings = obj.product_courses.filter(is_active=True).select_related("course")
        return [
            {
                "mapping_id": m.id,
                "primary_mapping": m.primary_mapping,
                "course": CourseSerializer(m.course).data
            }
            for m in mappings
        ]
