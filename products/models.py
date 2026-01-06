from utils import AbstractTimeCreateUpdate, AbstractIsDeleted, AbstractTimeCreation
from django.utils.translation import gettext_lazy as _
from manufacture_fees.models import ManufactureFees
from metal_types.models import MetalTypes
from brands.models import Brands
from django.db import models
from uuid import uuid4

def upload_photo(instance, filename):
    return f"products/{instance.product.title}/{str(instance.id).replace('-', '')}.{filename.rsplit('.', 1)[1]}"

class ProductPhotosQuerySet(models.QuerySet):
    def live(self, *args, **kwargs):
        kwargs['is_deleted'] = False
        return self.filter(*args, **kwargs)
    

class ProductsQuerySet(models.QuerySet):
    def live(self, *args, **kwargs):
        kwargs['is_deleted'] = False
        return self.filter(*args, **kwargs)

class Products(AbstractTimeCreateUpdate, AbstractIsDeleted, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    brand = models.ForeignKey(Brands, null=False, blank=False, on_delete=models.CASCADE)
    metal_type = models.ForeignKey(MetalTypes, null=False, blank=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=300, blank=False, null=False)
    description = models.TextField()
    weight = models.FloatField()
    kirat = models.FloatField()
    fitness = models.FloatField()
    is_available = models.BooleanField()
    is_popular = models.BooleanField(default=False)

    objects = ProductsQuerySet.as_manager()
    
    class Meta:
        verbose_name = _("product")
        verbose_name_plural = _("products")

    def __str__(self):
        return self.title
    
    @property
    def live_photos(self):
        return self.photos.live()

    @property
    def get_live_gold_price(self):
        from pricing.models import Pricing
        return Pricing.live_pricing().filter(type=1).values("local_buy")[0]

    @property
    def get_live_silver_price(self):
        from pricing.models import Pricing
        return Pricing.live_pricing().filter(type=2).values("local_buy")[0]
    
    
    @property
    def get_manufacture_fees(self):
        return ManufactureFees.objects.filter(type=self.metal_type.id, weight= self.weight).values('cashback', 'fees')
       
    
class ProductPhotos(AbstractTimeCreation, 
                    AbstractIsDeleted, 
                    models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    product = models.ForeignKey(Products, null=False, blank=False, on_delete=models.CASCADE, related_name="photos")
    photo = models.ImageField(upload_to=upload_photo)
    
    objects = ProductPhotosQuerySet.as_manager()

    class Meta:
        verbose_name = _("product photos")
        verbose_name_plural = _("product photos")

    def __str__(self):
        return self.product.title