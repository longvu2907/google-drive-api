from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from scheduler import tasks

def start():
    scheduler = BackgroundScheduler(job_defaults={'max_instances': 2})
    scheduler.add_job(tasks.update_database, 'interval', seconds=2)
    scheduler.start()