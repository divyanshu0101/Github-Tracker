import schedule
import time
from git_operations import clone_or_update_repositories
from logger import setup_logger

logger = setup_logger()

def schedule_task():
    schedule.every(24).hours.do(clone_or_update_repositories)
    logger.info("🔄 Scheduled to run every 24 hours.")

    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every 1 minute
