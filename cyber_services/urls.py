from django.urls import path
from . import views

app_name = 'cyber_services'

urlpatterns = [
    path('', views.service_list, name='service_list'),
    path('category/<str:category>/', views.service_list, name='service_list_by_category'),
    path('service/<slug:slug>/', views.service_detail, name='service_detail'),
    path('service/<slug:slug>/request/', views.request_service, name='request_service'),
    path('request/<int:request_id>/', views.request_detail, name='request_detail'),
    path('my-requests/', views.my_requests, name='my_requests'),
    path('request/<int:request_id>/upload-document/', views.upload_document, name='upload_document'),
] 