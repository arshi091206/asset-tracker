from apscheduler.schedulers.background import BackgroundScheduler
from .services import check_all_alerts

def start():
    scheduler=BackgroundScheduler()

    scheduler.add_job(
        check_all_alerts,
        "interval",
        minutes=5 
        #seconds=15
    )
    scheduler.start()

    print("scheduler started")