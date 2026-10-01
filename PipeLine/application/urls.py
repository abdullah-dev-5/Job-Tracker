from django.urls import path
from application import views

app_name = 'application'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard_view'),
    path('applications/', views.applications, name='applications'),
    path('applications_modal', views.applications_modal, name='app_modals'),
    path('api/company-logo/', views.company_logo, name='company_logo'),
]
