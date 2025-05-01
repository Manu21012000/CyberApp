from django import forms
from .models import BrandingRequest, BrandingAsset, DesignChart

class BrandingRequestForm(forms.ModelForm):
    class Meta:
        model = BrandingRequest
        fields = [
            'company_name',
            'company_description',
            'brand_guidelines',
            'target_audience',
            'color_preferences',
            'style_preferences',
            'additional_notes',
        ]
        widgets = {
            'company_description': forms.Textarea(attrs={'rows': 4}),
            'brand_guidelines': forms.Textarea(attrs={'rows': 4}),
            'target_audience': forms.Textarea(attrs={'rows': 4}),
            'style_preferences': forms.Textarea(attrs={'rows': 4}),
            'additional_notes': forms.Textarea(attrs={'rows': 4}),
        }

class BrandingAssetForm(forms.ModelForm):
    class Meta:
        model = BrandingAsset
        fields = ['asset_type', 'file', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class DesignChartForm(forms.ModelForm):
    class Meta:
        model = DesignChart
        fields = ['title', 'description', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        } 