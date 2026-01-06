from utils import AbstractTimeCreation, AbstractIsDeleted
from django.utils.translation import gettext_lazy as _
from django.db import models
from uuid import uuid4


class Faqs(AbstractTimeCreation, AbstractIsDeleted, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    question_body = models.TextField(null=False, blank=False)
    answer = models.TextField(null=False, blank=False)
    num_useful = models.BigIntegerField(default=0)
    num_unuseful = models.BigIntegerField(default=0)
    sort_order = models.IntegerField()

    class Meta:
        verbose_name = _("faqs")
        verbose_name_plural = _("faqs")
        ordering = ('sort_order',)

    def __str__(self):
        if len(self.question_body) > 4:
            return self.question_body[:4]

        return self.question_body
