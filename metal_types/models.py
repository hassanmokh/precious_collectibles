from utils import AbstractTimeCreation, AbstractIsDeleted
from django.utils.translation import gettext_lazy as _
from django.db import models
from uuid import uuid4

def upload_photo(instance, filename):
    return f"metals/{instance.name}/{str(instance.id).replace('-', '')}.{filename.rsplit('.', 1)[1]}"

class MetalTypes(AbstractTimeCreation, AbstractIsDeleted, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=100, null=False, blank=False)
    photo = models.ImageField(upload_to=upload_photo, null=True)
    
    class Meta:
        verbose_name = _("metal type")
        verbose_name_plural = _("metal types")

    def __str__(self):
        return self.name
