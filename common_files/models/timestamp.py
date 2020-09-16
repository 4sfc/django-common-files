"""Timestamp class"""

from django.contrib.auth.models import User
from django.db import models


class Timestamp(models.Model):
    """Abstract base class Timestamp model has created and modified fields"""

    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, blank=True, null=True,
                                   on_delete=models.CASCADE, related_name='+')
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, blank=True, null=True,
                                    on_delete=models.CASCADE, related_name='+')

    class Meta:
        abstract = True
