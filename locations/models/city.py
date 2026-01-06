from django.utils.translation import gettext_lazy as _
from django.db import models
from uuid import uuid4


class City(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    name = models.CharField(max_length=300, null=False, blank=False)
    name_ar = models.CharField(max_length=500, null=False, blank=False)

    class Meta:
        verbose_name = _("city")
        verbose_name_plural = _("cities")

    def __str__(self):
        return self.name

