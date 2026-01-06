from django.utils.translation import gettext_lazy as _
from django.db import models


class TypeMetal(models.IntegerChoices):
    GOLD = 1, _("Gold")
    SILVER = 2, _("Silver")
