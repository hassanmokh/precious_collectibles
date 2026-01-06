from django.db import models
from django.utils.timezone import now


class AbstractTimeCreation(models.Model):
    created_at = models.DateTimeField(default=now)

    class Meta:
        abstract = True


class AbstractIsDeleted(models.Model):
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


class AbstractTimeCreateUpdate(AbstractTimeCreation, models.Model):
    updated_at = models.DateTimeField(default=now)

    class Meta:
        abstract = True

