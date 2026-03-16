from django.db import models
from core.base_model import MasterModel


class Vendor(MasterModel):
    class Meta:
        db_table = "vendor"
        ordering = ["-created_at"]
