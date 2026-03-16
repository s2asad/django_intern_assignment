from django.db import models
from core.base_model import TimeStampedModel
from master_apps.course.models import Course
from master_apps.certification.models import Certification


class CourseCertificationMapping(TimeStampedModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="course_certifications")
    certification = models.ForeignKey(Certification, on_delete=models.CASCADE, related_name="certification_courses")
    primary_mapping = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "course_certification_mapping"
        unique_together = [("course", "certification")]
        ordering = ["-created_at"]

    def __str__(self):
        return f"Course {self.course} -> Certification {self.certification}"
