from django.db import models
from core.base_model import MasterModel


class Certification(MasterModel):
    class Meta:
        db_table = "certification"
        ordering = ["-created_at"]
