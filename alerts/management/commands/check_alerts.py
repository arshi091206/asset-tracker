from django.core.management.base import BaseCommand
from alerts.services import check_all_alerts

class Command(BaseCommand):
    help="check all active alerts and sends notification emails"

    def handle(self, *args, **kwargs):
        self.stdout.write("checking alerts..")
        check_all_alerts()
        self.stdout.write(
            self.style.SUCCESS("finished checking alerts.")
        )
        