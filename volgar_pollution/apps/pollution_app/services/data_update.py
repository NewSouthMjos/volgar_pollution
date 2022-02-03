from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from pollution_app.services.requests_pogodasv import new_data_point

logger = logging.getLogger(__name__)

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(new_data_point, 'cron', minute='10,30,50')
    scheduler.add_job(test_job, 'cron', minute='*')
    scheduler.start()

def test_job():
    logger.info('Executed test job done!')

start()