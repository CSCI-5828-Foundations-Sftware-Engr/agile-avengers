from celery import Celery
from celery.schedules import crontab
import src.config as config

class CeleryConfig:
    CELERY_IMPORTS = ('src.tasks')
    CELERY_TASK_RESULT_EXPIRES = 30
    CELERY_ACCEPT_CONTENT = ['json', 'msgpack', 'yaml']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    # CELERY_TIMEZONE = 'Asia/Seoul'
    CELERY_ENABLE_UTC = True
    CELERYBEAT_SCHEDULE = {
        "time_scheduler": {
            "task": "src.tasks.fetch_new_leaks", 
            "schedule": crontab(hour=f"*/{config.daily_fetch_time}", minute=0) #set schedule time
            # Ref: https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html
            # "schedule": 60
        }
    }

celery_app = Celery(__name__, broker=config.celery_broker)
celery_app.config_from_object(CeleryConfig)