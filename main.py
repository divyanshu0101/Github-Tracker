print("🚀 GitHub Tracker is starting...")
from .git_operations import clone_or_update_repositories
from scheduler import schedule_task
import time

if __name__ == "__main__":
    print("🚀 GitHub Tracker Started...")
    clone_or_update_repositories()  # Clone or update repos
    schedule_task()  # Schedule automatic execution

    while True:
        time.sleep(1)  # Keeps the scheduler running
