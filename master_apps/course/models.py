from django.db import models
from core.base_model import MasterModel


class Course(MasterModel):
    class Meta:
        db_table = "course"
        ordering = ["-created_at"]
