from django.core.management.base import BaseCommand
from main_app.models import PhoneVerification
from django.utils import timezone
from datetime import timedelta
from main_app.utils import send_verification_code

class Command(BaseCommand):
    help = 'Sends verification codes to unverified phone numbers'

    def handle(self, *args, **options):
        # Get unverified phone numbers that haven't received a code in the last 5 minutes
        five_minutes_ago = timezone.now() - timedelta(minutes=5)
        unverified_phones = PhoneVerification.objects.filter(
            is_verified=False,
            created_at__lte=five_minutes_ago
        )
        
        count = 0
        for phone_verification in unverified_phones:
            try:
                # Try WhatsApp first, fall back to SMS if it fails
                success, result = send_verification_code(
                    phone_verification.phone_number,
                    phone_verification.verification_code,
                    method='whatsapp'
                )
                
                if not success:
                    # Fall back to SMS
                    success, result = send_verification_code(
                        phone_verification.phone_number,
                        phone_verification.verification_code,
                        method='sms'
                    )
                
                if success:
                    # Update the created_at timestamp to prevent immediate resending
                    phone_verification.created_at = timezone.now()
                    phone_verification.save()
                    
                    count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'Sent verification code to {phone_verification.phone_number}')
                    )
                else:
                    self.stdout.write(
                        self.style.ERROR(f'Failed to send verification code to {phone_verification.phone_number}: {result}')
                    )
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Failed to send verification code to {phone_verification.phone_number}: {str(e)}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully sent {count} verification codes')
        ) 