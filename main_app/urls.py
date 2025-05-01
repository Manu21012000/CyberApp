from django.urls import path
from . import views

app_name = 'main_app'

urlpatterns = [
	path('', views.index, name='index'),
	path('test-email/', views.test_email, name='test_email'),
	path('check-verification/', views.check_verification, name='check_verification'),
	path('verify-phone/', views.verify_phone, name='verify_phone'),
	path('resend-phone-verification/', views.resend_phone_verification, name='resend_phone_verification'),
]