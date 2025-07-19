# services/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('providers/', views.ProviderListView.as_view(), name='providers'),
    path('book/', views.book_service, name='book_service'),
    path('history/', views.user_history, name='user_history'),
    path('register/', views.register, name='register'),
    path('create-provider/', views.create_provider, name='create_provider'),
    # services/urls.py
    path('provider-dashboard/', views.provider_dashboard, name='provider_dashboard'),
    path('about/', views.about_page, name='about'),
    path('contact/', views.contact_page, name='contact'),


]

