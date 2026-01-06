from django.utils.translation import gettext_lazy as _
from metal_types.models import MetalTypes
from django.db import models


class ManufactureFees(models.Model):
    cashback = models.DecimalField(decimal_places=2, max_digits=6)
    fees = models.DecimalField(decimal_places=2, max_digits=6)
    type = models.ForeignKey(MetalTypes, null=False, blank=False, related_query_name="manufacture_fees", on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=16, decimal_places=2)
    
    class Meta:
        verbose_name = _("manufacture fees")
        verbose_name_plural = _("manufacture fees")
        unique_together = ('type', 'weight')
    
    
    def __str__(self):
        return f"{self.type}-{self.weight}"
    
