from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Service, ServiceRequest, Document, ServiceField, ServiceFieldValue
from .forms import ServiceRequestForm, DocumentForm
from django.views.generic import ListView, DetailView

def service_list(request, category=None):
    services = Service.objects.filter(is_active=True)
    if category:
        services = services.filter(category=category)
    
    categories = Service.CATEGORY_CHOICES
    paginator = Paginator(services, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'cyber_services/service/list.html', {
        'page_obj': page_obj,
        'categories': categories,
        'current_category': category,
    })

def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug, is_active=True)
    return render(request, 'cyber_services/service/detail.html', {'service': service})

@login_required
def request_service(request, slug):
    service = get_object_or_404(Service, slug=slug, is_active=True)
    
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST)
        if form.is_valid():
            service_request = form.save(commit=False)
            service_request.user = request.user
            service_request.service = service
            service_request.save()
            
            # Handle document uploads
            for file in request.FILES.getlist('documents'):
                Document.objects.create(
                    service_request=service_request,
                    document_type=request.POST.get('document_type'),
                    file=file
                )
            
            # Handle custom fields
            for field in service.fields.all():
                value = request.POST.get(f'field_{field.id}')
                if value:
                    ServiceFieldValue.objects.create(
                        service_request=service_request,
                        field=field,
                        value=value
                    )
            
            messages.success(request, 'Your service request has been submitted successfully!')
            return redirect('cyber_services:request_detail', request_id=service_request.id)
    else:
        form = ServiceRequestForm()
    
    return render(request, 'cyber_services/service/request.html', {
        'service': service,
        'form': form,
    })

@login_required
def request_detail(request, request_id):
    service_request = get_object_or_404(ServiceRequest, id=request_id, user=request.user)
    return render(request, 'cyber_services/request/detail.html', {'request': service_request})

@login_required
def my_requests(request):
    requests = ServiceRequest.objects.filter(user=request.user).order_by('-created_at')
    paginator = Paginator(requests, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'cyber_services/request/list.html', {'page_obj': page_obj})

@login_required
def upload_document(request, request_id):
    service_request = get_object_or_404(ServiceRequest, id=request_id, user=request.user)
    
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.service_request = service_request
            document.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})
    
    return JsonResponse({'success': False, 'errors': 'Invalid request method'})

class ServiceListView(ListView):
    model = Service
    template_name = 'cyber_services/service_list.html'
    context_object_name = 'services'
    paginate_by = 10

class ServiceDetailView(DetailView):
    model = Service
    template_name = 'cyber_services/service_detail.html'
    context_object_name = 'service'
