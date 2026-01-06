from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
from products.models import Products
from users.models import User
from django.db import models
from uuid import uuid4


def upload_bill_scan(instance, filename):
    fname = now().__str__().replace("-", "_").replace(" ", "_").replace(":", "_").rsplit(".", 1)[0]

    return f"balances/{instance.user.username}/{instance.product.title}_{fname}.{filename.rsplit('.', 1)[1]}"


class Balances(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    product = models.ForeignKey(Products, blank=False, null=False, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(blank=False, null=False)
    purchase_price = models.FloatField()
    gm_price = models.FloatField()
    packing_per_gm = models.FloatField()
    cashback_per_gm = models.FloatField()
    is_available = models.BooleanField(default=True)
    bill_scan = models.ImageField(upload_to=upload_bill_scan)

    class Meta:
        verbose_name = _("balance")
        verbose_name_plural = _("balances")

    def __str__(self):
        return f"{self.user.first_name}: {self.product.title}"
