from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .models import BrandingProduct, ProductImage, BrandingRequest, BrandingAsset, DesignChart
from .forms import BrandingRequestForm, BrandingAssetForm, DesignChartForm

# Create your views here.

class ProductListView(ListView):
    model = BrandingProduct
    template_name = 'branding_services/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        queryset = BrandingProduct.objects.all()
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = BrandingProduct.CATEGORY_CHOICES
        return context

class ProductDetailView(DetailView):
    model = BrandingProduct
    template_name = 'branding_services/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context['images'] = product.images.all()
        return context

@login_required
def request_branding(request, pk):
    product = get_object_or_404(BrandingProduct, pk=pk)
    
    if request.method == 'POST':
        request_form = BrandingRequestForm(request.POST)
        asset_form = BrandingAssetForm(request.POST, request.FILES)
        chart_form = DesignChartForm(request.POST, request.FILES)
        
        if request_form.is_valid():
            branding_request = request_form.save(commit=False)
            branding_request.user = request.user
            branding_request.product = product
            branding_request.save()
            
            if asset_form.is_valid():
                asset = asset_form.save(commit=False)
                asset.request = branding_request
                asset.save()
            
            if chart_form.is_valid():
                chart = chart_form.save(commit=False)
                chart.request = branding_request
                chart.save()
            
            messages.success(request, 'Your branding request has been submitted successfully!')
            return redirect('branding_services:request_detail', pk=branding_request.pk)
    else:
        request_form = BrandingRequestForm()
        asset_form = BrandingAssetForm()
        chart_form = DesignChartForm()
    
    return render(request, 'branding_services/request_form.html', {
        'product': product,
        'request_form': request_form,
        'asset_form': asset_form,
        'chart_form': chart_form,
    })

@login_required
def request_detail(request, pk):
    branding_request = get_object_or_404(BrandingRequest, pk=pk, user=request.user)
    return render(request, 'branding_services/request_detail.html', {
        'request': branding_request,
    })

@login_required
def my_requests(request):
    requests = BrandingRequest.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'branding_services/my_requests.html', {
        'requests': requests,
    })
