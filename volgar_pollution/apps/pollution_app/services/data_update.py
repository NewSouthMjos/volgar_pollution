from datetime import datetime
import logging

# from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
# from pollution_app.services.requests_pogodasv import new_data_point

logger = logging.getLogger(__name__)

def start():
    scheduler = BlockingScheduler()
    # scheduler.add_job(new_data_point, 'cron', minute='10,30,50')
    scheduler.add_job(test_job, 'interval', minutes=1)
    scheduler.start()

def test_job():
    logger.info('Executed test job done!')

start()

# from apscheduler.schedulers.blocking import BlockingScheduler

# sched = BlockingScheduler()

# @sched.scheduled_job('interval', minutes=1)
# def timed_job():
#     print('This job is run every three minutes.')

# sched.start()