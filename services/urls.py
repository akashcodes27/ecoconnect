# services/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('providers/', views.ProviderListView.as_view(), name='providers'),
    path('book/', views.book_service, name='book_service'),
    path('upload-cert/', views.upload_certification, name='upload_cert'),
    path('history/', views.user_history, name='user_history'),
    path('register/', views.register, name='register'),
]
