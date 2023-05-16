from __future__ import absolute_import, unicode_literals

import os 
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oeccore.settings')

app = Celery('oeccore')

app.config_from_object('django.conf:settings', namespace= 'CELERY')


# to automatically search for tasks in apps
app.autodiscover_tasks()