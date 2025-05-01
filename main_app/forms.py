from django import forms
from allauth.account.forms import SignupForm
from phonenumber_field.formfields import PhoneNumberField
import random
from main_app.utils import send_verification_code

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')
    phone_number = PhoneNumberField(label='Phone Number')
    
    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()

        # Generate verification code
        verification_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        
        # Create phone verification record
        from .models import PhoneVerification
        phone_verification = PhoneVerification.objects.create(
            user=user,
            phone_number=self.cleaned_data['phone_number'],
            verification_code=verification_code
        )

        # Send verification code
        success, result = send_verification_code(
            phone_verification.phone_number,
            verification_code,
            method='whatsapp'  # Try WhatsApp first
        )
        
        if not success:
            # Fall back to SMS
            success, result = send_verification_code(
                phone_verification.phone_number,
                verification_code,
                method='sms'
            )
        
        if not success:
            # Log the error but don't prevent account creation
            print(f"Failed to send verification code: {result}")
        
        return user 