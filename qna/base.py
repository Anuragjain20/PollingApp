import datetime
import uuid

from django.db import models


# Create your models here.
class BaseModel(models.Model):
    """A base model to deal with all the asbtracrt level model creations"""
    class Meta:
        abstract = True

    # uuid field
    id = models.UUIDField(default=uuid.uuid4,
                           primary_key=True,
                           editable=False)

    # date fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
