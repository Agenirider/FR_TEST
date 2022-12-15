import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fr_sender.settings')

celery_app = Celery('fr_sender')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()

celery_app.conf.beat_schedule = {
    'get_new_tasks': {
        'task': 'sender.tasks.get_new_tasks',
        'schedule': crontab()  # execute every minute
    },
    'send_statistics': {
        'task': 'sender.tasks.send_statistics',
        'schedule': crontab(minute=0, hour=0)
    }
}
