# from __future__ import absolute_import, unicode_literals
# from django.conf import settings
# from celery import Celery
# from celery.schedules import crontab
# import os

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "precious_collectibles.settings.local")

# app = Celery("precious_collectibles")
# app.config_from_object("django.conf:settings", namespace="CELERY")
# app.conf.beat_schedule = {
#     'get_live_price_every_minute': {
#         'task': 'charts.tasks.live_price',
#         'schedule': crontab(minute='*/1')  # Run every 1 minute
#     },
# }
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
