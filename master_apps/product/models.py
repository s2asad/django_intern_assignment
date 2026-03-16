from django.db import models
from core.base_model import MasterModel


class Product(MasterModel):
    class Meta:
        db_table = "product"
        ordering = ["-created_at"]
