from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone

class PhoneVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='phone_verification')
    phone_number = PhoneNumberField(unique=True)
    verification_code = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    verified_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} - {self.phone_number}"

class UnverifiedAccountCleanup(models.Model):
    last_cleanup = models.DateTimeField(auto_now=True)

    @classmethod
    def cleanup_unverified_accounts(cls):
        from django.conf import settings
        from django.utils import timezone
        from datetime import timedelta

        # Get the threshold date
        threshold_date = timezone.now() - timedelta(days=settings.ACCOUNT_UNVERIFIED_ACCOUNT_DELETION_DAYS)
        
        # Get unverified accounts older than threshold
        unverified_accounts = User.objects.filter(
            is_active=False,
            date_joined__lt=threshold_date
        )
        
        # Delete the accounts
        count = unverified_accounts.count()
        unverified_accounts.delete()
        
        # Update or create the cleanup record
        cls.objects.update_or_create(
            id=1,
            defaults={'last_cleanup': timezone.now()}
        )
        
        return count
