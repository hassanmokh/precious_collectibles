from django.utils.translation import gettext_lazy as _
from utils import TypeMetal, AbstractTimeCreation
from django.db import models
from uuid import uuid4


class Charts(AbstractTimeCreation, models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    type = models.SmallIntegerField(choices=TypeMetal.choices, blank=False, null=False)
    world_sell_price = models.DecimalField(max_digits=8, decimal_places=2)
    world_buy_price = models.DecimalField(max_digits=8, decimal_places=2)
    local_sell_price = models.DecimalField(max_digits=8, decimal_places=2)
    local_buy_price = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        verbose_name = _("chart")
        verbose_name_plural = _("charts")
        ordering = ('created_at',)

    def __str__(self):
        return f'{self.get_type_display()}:{self.local_buy_price}'

    @classmethod
    def create_charts(cls, **data):
        Charts.objects.get_or_create(**data)