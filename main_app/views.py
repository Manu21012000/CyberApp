from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from allauth.account.models import EmailAddress
from .models import PhoneVerification
from django.utils import timezone

# Create your views here
def home(request):
	return render(request, "base/index.html")

def index(request):
    """
    Main landing page view that serves as the entry point for the entire application.
    Displays cards for Cyber Services, Branding Services, and E-commerce sections.
    """
    return render(request, 'main_app/index.html')

def test_email(request):
    try:
        send_mail(
            'Test Email',
            'This is a test email from your Django application.',
            settings.EMAIL_HOST_USER,
            [settings.EMAIL_HOST_USER],
            fail_silently=False,
        )
        return HttpResponse('Test email sent successfully!')
    except Exception as e:
        return HttpResponse(f'Error sending email: {str(e)}')

@login_required
def check_verification(request):
    if not request.user.is_authenticated:
        return redirect('account_login')
    
    email_address = EmailAddress.objects.get_primary(request.user)
    if not email_address or not email_address.verified:
        messages.warning(request, 'Please verify your email address to access all features.')
        return render(request, 'account/verification_sent.html')
    
    return redirect('home')

@login_required
def verify_phone(request):
    if request.method == 'POST':
        verification_code = request.POST.get('verification_code')
        try:
            phone_verification = PhoneVerification.objects.get(
                user=request.user,
                verification_code=verification_code,
                is_verified=False
            )
            
            # Check if code is expired (5 minutes)
            if (timezone.now() - phone_verification.created_at).total_seconds() > 300:
                messages.error(request, 'Verification code has expired. Please request a new one.')
                return redirect('verify_phone')
            
            phone_verification.is_verified = True
            phone_verification.verified_at = timezone.now()
            phone_verification.save()
            
            messages.success(request, 'Phone number verified successfully!')
            return redirect('check_verification')
            
        except PhoneVerification.DoesNotExist:
            messages.error(request, 'Invalid verification code. Please try again.')
            return redirect('verify_phone')
    
    return render(request, 'main_app/verify_phone.html')

@login_required
def resend_phone_verification(request):
    try:
        phone_verification = PhoneVerification.objects.get(
            user=request.user,
            is_verified=False
        )
        
        # Generate new verification code
        import random
        new_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        phone_verification.verification_code = new_code
        phone_verification.created_at = timezone.now()
        phone_verification.save()
        
        # TODO: Send new verification code via WhatsApp/SMS
        
        messages.success(request, 'New verification code sent to your phone number.')
        return redirect('verify_phone')
        
    except PhoneVerification.DoesNotExist:
        messages.error(request, 'No pending phone verification found.')
        return redirect('check_verification')