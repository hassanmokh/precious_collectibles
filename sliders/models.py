from utils import AbstractIsDeleted, AbstractTimeCreation
from django.utils.translation import gettext_lazy as _
from django.db import models
from uuid import uuid4

def upload_photo(instance, filename):
    return f"sliders/{str(instance.id).replace('-', '')}.{filename.rsplit('.', 1)[1]}"


class SliderQuerySet(models.QuerySet):
    def live(self, *args, **kwargs):
        kwargs['is_deleted'] = False
        return self.filter(*args, **kwargs)

class Slider(AbstractTimeCreation, 
             AbstractIsDeleted,
             models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    photo = models.ImageField(upload_to=upload_photo)
    redirect_url = models.URLField(null=True, blank=True)
    
    objects = SliderQuerySet.as_manager()
    
    class Meta:
        verbose_name = _("slider")
        verbose_name_plural = _("sliders")
    