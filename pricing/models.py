from django.utils.translation import gettext_lazy as _
from utils import TypeMetal, AbstractTimeCreateUpdate
from django.db import models
from uuid import uuid4

class Pricing(AbstractTimeCreateUpdate, models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    type = models.SmallIntegerField(choices=TypeMetal.choices, blank=False, null=False)
    local_sell = models.DecimalField('sell', max_digits=8, decimal_places=2)
    local_buy = models.DecimalField('buy', max_digits=8, decimal_places=2)
    world_sell = models.DecimalField('world sell', max_digits=8, decimal_places=2, null=True, blank=True)
    world_buy = models.DecimalField('world buy', max_digits=8, decimal_places=2, null=True, blank=True)
    old = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = _("pricing")
        verbose_name_plural = _("pricing")
        ordering = ('old', '-type',)
        
    def __str__(self):
        return f'{self.get_type_display()} -> {self.local_buy}'
    
    def save(self, *args, **kwargs):
        if kwargs.get('force_insert', False):
            Pricing.objects.filter(type=self.type, old=False).update(old=True)
        return super().save(*args, **kwargs)
    
    @classmethod
    def live_pricing(cls):
        return Pricing.objects.filter(old=False)