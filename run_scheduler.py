import os
import time
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "asset_tracker.settings")
django.setup()

from alerts.scheduler import start

start()

while True:
    time.sleep(60)