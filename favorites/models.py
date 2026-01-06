from django.utils.translation import gettext_lazy as _
from utils import AbstractTimeCreation
from products.models import Products
from users.models import User
from django.db import models
from uuid import uuid4


class Favorites(AbstractTimeCreation, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    product = models.ForeignKey(Products, blank=False, null=False, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("favorite")
        verbose_name_plural = _("favorites")

    def __str__(self):
        return f"{self.user.first_name}:{self.product.title}"
