from django import forms
from allauth.account.forms import SignupForm
from phonenumber_field.formfields import PhoneNumberField
import random

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
        PhoneVerification.objects.create(
            user=user,
            phone_number=self.cleaned_data['phone_number'],
            verification_code=verification_code
        )

        # TODO: Send verification code via WhatsApp/SMS
        # You'll need to implement this based on your preferred service provider
        
        return user 