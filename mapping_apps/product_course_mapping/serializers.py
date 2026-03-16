from rest_framework import serializers
from .models import ProductCourseMapping


class ProductCourseMappingSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    course_name = serializers.CharField(source="course.name", read_only=True)

    class Meta:
        model = ProductCourseMapping
        fields = ["id", "product", "product_name", "course", "course_name",
                  "primary_mapping", "is_active", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate(self, data):
        instance = self.instance
        product = data.get("product", instance.product if instance else None)
        course = data.get("course", instance.course if instance else None)
        primary_mapping = data.get("primary_mapping", instance.primary_mapping if instance else False)

        qs = ProductCourseMapping.objects.filter(product=product, course=course)
        if instance:
            qs = qs.exclude(pk=instance.pk)
        if qs.exists():
            raise serializers.ValidationError("This product-course mapping already exists.")

        if primary_mapping:
            primary_qs = ProductCourseMapping.objects.filter(product=product, primary_mapping=True)
            if instance:
                primary_qs = primary_qs.exclude(pk=instance.pk)
            if primary_qs.exists():
                raise serializers.ValidationError(
                    "This product already has a primary course mapping. Only one primary mapping is allowed per product."
                )
        return data
