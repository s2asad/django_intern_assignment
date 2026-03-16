from rest_framework import serializers
from .models import Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["id", "name", "code", "description", "is_active", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_code(self, value):
        instance = self.instance
        qs = Course.objects.filter(code=value)
        if instance:
            qs = qs.exclude(pk=instance.pk)
        if qs.exists():
            raise serializers.ValidationError("A course with this code already exists.")
        return value


class CourseNestedSerializer(serializers.ModelSerializer):
    """Returns course with all its mapped certifications (nested)."""
    certifications = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ["id", "name", "code", "description", "is_active", "certifications"]

    def get_certifications(self, obj):
        from master_apps.certification.serializers import CertificationSerializer
        mappings = obj.course_certifications.filter(is_active=True).select_related("certification")
        return [
            {
                "mapping_id": m.id,
                "primary_mapping": m.primary_mapping,
                "certification": CertificationSerializer(m.certification).data
            }
            for m in mappings
        ]
