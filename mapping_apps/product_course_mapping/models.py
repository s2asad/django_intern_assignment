from django.db import models
from core.base_model import TimeStampedModel
from master_apps.product.models import Product
from master_apps.course.models import Course


class ProductCourseMapping(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_courses")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="course_products")
    primary_mapping = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "product_course_mapping"
        unique_together = [("product", "course")]
        ordering = ["-created_at"]

    def __str__(self):
        return f"Product {self.product} -> Course {self.course}"
