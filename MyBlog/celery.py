from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MyBlog.settings')

app = Celery('task')    # 项目名

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')  # 使用django的session

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()    # 项目下所有app的celery任务发现


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))