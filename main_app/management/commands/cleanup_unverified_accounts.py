from django.core.management.base import BaseCommand
from main_app.models import UnverifiedAccountCleanup

class Command(BaseCommand):
    help = 'Clean up unverified accounts that are older than the specified days'

    def handle(self, *args, **options):
        try:
            count = UnverifiedAccountCleanup.cleanup_unverified_accounts()
            self.stdout.write(
                self.style.SUCCESS(f'Successfully cleaned up {count} unverified accounts')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error cleaning up unverified accounts: {str(e)}')
            ) 