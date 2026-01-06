from django.db import models
from uuid import uuid4
from django.utils.translation import gettext_lazy as _
from utils import (
    AbstractTimeCreateUpdate, AbstractTimeCreation,
    AbstractIsDeleted
)

def upload_photo(instance, filename):
    title = instance.album.title
    return f"album/{title}/{title}_{str(instance.id).replace('-', '')}.{filename.rsplit('.', 1)[1]}"


class AlbumQuerySet(models.QuerySet):
    def live(self, *args, **kwargs):
        kwargs['is_deleted'] = False
        return self.filter(*args, **kwargs)

class PhotoQuerySet(models.QuerySet):
    def live(self, *args, **kwargs):
        kwargs['is_deleted'] = False
        return self.filter(*args, **kwargs)


class Album(AbstractTimeCreateUpdate, 
            AbstractIsDeleted, 
            models.Model):
    
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    title = models.CharField(max_length=300)
    title_ar = models.CharField(max_length=400)
    description = models.TextField()
    description_ar = models.TextField()
    
    objects = AlbumQuerySet.as_manager()
    
    class Meta:
        verbose_name = _("album")
        verbose_name_plural = _("albums")
        ordering = ('-created_at',)   
        
    @property
    def photos(self):
        return self.photos.all()
    
    @property
    def live_photos(self):
        return self.photos.live()
    
    def __str__(self):
        return self.title
    


class Photo(AbstractTimeCreateUpdate,
            AbstractIsDeleted,
            models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, null=False, blank=False, related_name="photos")
    url = models.ImageField(upload_to=upload_photo)
    
    objects = PhotoQuerySet.as_manager()
    
    class Meta:
        verbose_name = _("photo")
        verbose_name_plural = _("photos")
        ordering = ('-created_at',)   
    
    
    def __str__(self):
        return str(self.id)