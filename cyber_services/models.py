from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.urls import reverse

class Service(models.Model):
    CATEGORY_CHOICES = [
        ('kra', 'KRA Services'),
        ('ecitizen', 'E-Citizen Services'),
        ('nssf', 'NSSF Services'),
        ('nhif', 'NHIF Services'),
        ('ntsa', 'NTSA Services'),
        ('other', 'Other Services'),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    processing_time = models.CharField(max_length=100, help_text="Estimated processing time")
    requirements = models.TextField(help_text="Required documents and information")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('cyber_services:service_detail', kwargs={'pk': self.pk})

class ServiceRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    additional_info = models.TextField(blank=True, help_text="Any additional information for processing")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.service.name}"

class Document(models.Model):
    DOCUMENT_TYPES = [
        ('id', 'National ID'),
        ('passport', 'Passport'),
        ('kra_pin', 'KRA PIN Certificate'),
        ('birth_certificate', 'Birth Certificate'),
        ('other', 'Other'),
    ]

    service_request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    file = models.FileField(
        upload_to='documents/%Y/%m/%d/',
        validators=[FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png'])]
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_document_type_display()} - {self.service_request}"

class ServiceField(models.Model):
    FIELD_TYPES = [
        ('text', 'Text'),
        ('number', 'Number'),
        ('email', 'Email'),
        ('date', 'Date'),
        ('file', 'File'),
    ]

    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='fields')
    name = models.CharField(max_length=100)
    field_type = models.CharField(max_length=20, choices=FIELD_TYPES)
    is_required = models.BooleanField(default=True)
    description = models.TextField(blank=True, help_text="Field description or instructions")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.service.name} - {self.name}"

class ServiceFieldValue(models.Model):
    service_request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE, related_name='field_values')
    field = models.ForeignKey(ServiceField, on_delete=models.CASCADE)
    value = models.TextField()

    def __str__(self):
        return f"{self.service_request} - {self.field.name}"
