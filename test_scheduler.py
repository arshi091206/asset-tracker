import os
import django

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "asset_tracker.settings"
)
django.setup()

from alerts.services import check_all_alerts
check_all_alerts()
print("Done")