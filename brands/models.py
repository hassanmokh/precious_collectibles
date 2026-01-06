from utils import AbstractIsDeleted, AbstractTimeCreateUpdate
from django.utils.translation import gettext_lazy as _
from django.db import models
from uuid import uuid4

def upload_photo(instance, filename):
    return f"brands/{instance.name}/{str(instance.id).replace('-', '')}.{filename.rsplit('.', 1)[1]}"

class Brands(AbstractTimeCreateUpdate, AbstractIsDeleted, models.Model):

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=150, null=False, blank=False)
    photo = models.ImageField(upload_to=upload_photo, null=True)
    is_popular = models.BooleanField(default=False)
    
    
    class Meta:
        verbose_name = _("brand")
        verbose_name_plural = _("brands")

    def __str__(self):
        return self.name

