from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid


class UUIDBase(models.Model):
    """
    Abstract Base class
    uid: uuid4
    created_date: date time stamp
    updated_date: last updated
    """
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=False)
    created_date = models.DateTimeField(
        _("Created Date"), auto_now_add=True, auto_now=False)
    updated_date = models.DateTimeField(
        _("Updated Date"), auto_now_add=False, auto_now=True)

    class Meta:
        abstract = True