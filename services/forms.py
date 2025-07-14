# services/forms.py
from django import forms
from .models import Booking, ServiceProvider
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class BookingForm(forms.ModelForm):
    booking_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Booking
        fields = ['provider', 'booking_date']


class ProviderRegistrationForm(forms.ModelForm):
    class Meta:
        model = ServiceProvider
        fields = ['name', 'service_type', 'location', 'certification']


class UploadCertificationForm(forms.ModelForm):
    class Meta:
        model = ServiceProvider
        fields = ['certification']


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
