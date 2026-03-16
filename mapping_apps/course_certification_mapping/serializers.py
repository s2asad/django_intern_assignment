from rest_framework import serializers
from .models import CourseCertificationMapping


class CourseCertificationMappingSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source="course.name", read_only=True)
    certification_name = serializers.CharField(source="certification.name", read_only=True)

    class Meta:
        model = CourseCertificationMapping
        fields = ["id", "course", "course_name", "certification", "certification_name",
                  "primary_mapping", "is_active", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate(self, data):
        instance = self.instance
        course = data.get("course", instance.course if instance else None)
        certification = data.get("certification", instance.certification if instance else None)
        primary_mapping = data.get("primary_mapping", instance.primary_mapping if instance else False)

        qs = CourseCertificationMapping.objects.filter(course=course, certification=certification)
        if instance:
            qs = qs.exclude(pk=instance.pk)
        if qs.exists():
            raise serializers.ValidationError("This course-certification mapping already exists.")

        if primary_mapping:
            primary_qs = CourseCertificationMapping.objects.filter(course=course, primary_mapping=True)
            if instance:
                primary_qs = primary_qs.exclude(pk=instance.pk)
            if primary_qs.exists():
                raise serializers.ValidationError(
                    "This course already has a primary certification mapping. Only one primary mapping is allowed per course."
                )
        return data
