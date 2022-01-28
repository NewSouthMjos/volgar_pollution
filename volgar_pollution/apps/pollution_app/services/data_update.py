from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from pollution_app.services.requests_pogodasv import new_data_point

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(new_data_point, 'cron', minute='10,30,50')
    scheduler.start()