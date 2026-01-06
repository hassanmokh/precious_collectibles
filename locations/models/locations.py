from django.utils.translation import gettext_lazy as _
from django.db import models


class Locations(models.Model):
    merchant_name = models.CharField(max_length=200)
    lat = models.FloatField()
    lng = models.FloatField()
    address_line_1 = models.CharField(max_length=400)
    address_line_2 = models.CharField(max_length=400, blank=True, null=True)
    city = models.ForeignKey('locations.City', null=False, blank=False, on_delete=models.CASCADE)
    governorate = models.ForeignKey('locations.Governorate', null=False, blank=False, on_delete=models.CASCADE)
    working_time = models.TextField()

    class Meta:
        verbose_name = _("location")
        verbose_name_plural = _("locations")

    def __str__(self):
        return self.merchant_name
