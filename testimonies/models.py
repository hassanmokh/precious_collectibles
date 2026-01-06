from utils import AbstractTimeCreateUpdate, AbstractIsDeleted
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
from django.db import models


fname = now().__str__().replace("-", "_").replace(" ", "_").replace(":", "_").rsplit(".", 1)[0]


def upload_photo(instance, filename):
    return f"testimonies/photos/{instance.full_name.replace(' ', '_')}_{fname}.{filename.rsplit('.', 1)[1]}"


def upload_screenshot(instance, filename):
    return f"testimonies/screenshots/{instance.full_name.replace(' ', '_')}_{fname}.{filename.rsplit('.', 1)[1]}"


class TestimoniesManager(models.QuerySet):
    def live(self, *args, **kwargs):
        kwargs['is_deleted'] = False
        return self.filter(*args, **kwargs)


class Testimonies(AbstractTimeCreateUpdate, AbstractIsDeleted, models.Model):
    image = models.ImageField(upload_to=upload_photo)
    full_name = models.CharField(max_length=120, blank=False, null=False)
    body = models.TextField()
    screenshot = models.ImageField(upload_to=upload_screenshot)
    testimony_date = models.DateField()

    objects = TestimoniesManager.as_manager()

    class Meta:
        verbose_name = _("testimony")
        verbose_name_plural = _("testimonies")

    def __str__(self):
        if len(self.body) > 4:
            return self.body[:4]

        return self.body
