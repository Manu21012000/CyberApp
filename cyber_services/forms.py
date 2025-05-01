from django import forms
from .models import ServiceRequest, Document, ServiceField

class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['additional_info']
        widgets = {
            'additional_info': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border rounded-md',
                'rows': 4,
                'placeholder': 'Any additional information for processing your request...'
            })
        }

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['document_type', 'file']
        widgets = {
            'document_type': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border rounded-md'
            }),
            'file': forms.FileInput(attrs={
                'class': 'w-full px-3 py-2 border rounded-md',
                'accept': '.pdf,.jpg,.jpeg,.png'
            })
        }

def get_service_field_form(service):
    """Dynamically create a form with fields based on the service's requirements"""
    class DynamicServiceForm(forms.Form):
        def __init__(self, *args, **kwargs):
            super(DynamicServiceForm, self).__init__(*args, **kwargs)
            
            for field in service.fields.all():
                field_name = f'field_{field.id}'
                field_class = {
                    'text': forms.CharField,
                    'number': forms.IntegerField,
                    'email': forms.EmailField,
                    'date': forms.DateField,
                    'file': forms.FileField,
                }[field.field_type]
                
                field_kwargs = {
                    'required': field.is_required,
                    'label': field.name,
                    'help_text': field.description,
                }
                
                if field.field_type == 'text':
                    field_kwargs['widget'] = forms.TextInput(attrs={
                        'class': 'w-full px-3 py-2 border rounded-md'
                    })
                elif field.field_type == 'number':
                    field_kwargs['widget'] = forms.NumberInput(attrs={
                        'class': 'w-full px-3 py-2 border rounded-md'
                    })
                elif field.field_type == 'email':
                    field_kwargs['widget'] = forms.EmailInput(attrs={
                        'class': 'w-full px-3 py-2 border rounded-md'
                    })
                elif field.field_type == 'date':
                    field_kwargs['widget'] = forms.DateInput(attrs={
                        'class': 'w-full px-3 py-2 border rounded-md',
                        'type': 'date'
                    })
                elif field.field_type == 'file':
                    field_kwargs['widget'] = forms.FileInput(attrs={
                        'class': 'w-full px-3 py-2 border rounded-md',
                        'accept': '.pdf,.jpg,.jpeg,.png'
                    })
                
                self.fields[field_name] = field_class(**field_kwargs)
    
    return DynamicServiceForm 