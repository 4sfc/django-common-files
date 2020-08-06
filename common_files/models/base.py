"""Base class"""

from django.db import models

from common_files.models.timestamp import Timestamp


class Base(Timestamp):
    """Abstract base class Base has label, value, and active fields"""

    label = models.CharField(max_length=191, unique=True)
    value = models.CharField(max_length=10, unique=True)
    active = models.BooleanField(default=True, null=False)

    def __str__(self):
        return self.label

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['label', 'value'],
                                    name='unique_label_value')
        ]
        abstract = True
