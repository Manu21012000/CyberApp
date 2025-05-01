from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class BrandingProduct(models.Model):
    CATEGORY_CHOICES = [
        ('graphic_design', 'Graphic Design'),
        ('mug_printing', 'Mug Printing'),
        ('banner_printing', 'Banner Printing & Design'),
        ('rollup_banner', 'Roll Up Banners'),
        ('advertising', 'Advertising'),
        ('tshirt_printing', 'T-Shirt Printing'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    processing_time = models.CharField(max_length=100, help_text="Estimated processing time")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('branding_services:product_detail', kwargs={'pk': self.pk})

class ProductImage(models.Model):
    product = models.ForeignKey(BrandingProduct, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='branding_products/')
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.product.name}"

    class Meta:
        ordering = ['-is_primary', 'created_at']

class BrandingRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(BrandingProduct, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200)
    company_description = models.TextField()
    brand_guidelines = models.TextField(blank=True, help_text="Any existing brand guidelines or preferences")
    target_audience = models.TextField(help_text="Description of target audience")
    color_preferences = models.CharField(max_length=200, blank=True)
    style_preferences = models.TextField(blank=True)
    additional_notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.company_name} - {self.product.name}"

class BrandingAsset(models.Model):
    ASSET_TYPES = [
        ('logo', 'Logo'),
        ('brand_guide', 'Brand Guidelines'),
        ('color_palette', 'Color Palette'),
        ('typography', 'Typography Guide'),
        ('other', 'Other'),
    ]

    request = models.ForeignKey(BrandingRequest, related_name='assets', on_delete=models.CASCADE)
    asset_type = models.CharField(max_length=50, choices=ASSET_TYPES)
    file = models.FileField(upload_to='branding_assets/')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_asset_type_display()} for {self.request.company_name}"

class DesignChart(models.Model):
    request = models.ForeignKey(BrandingRequest, related_name='charts', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='design_charts/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chart for {self.request.company_name}"
