# services/forms.py
from django import forms
from .models import Booking, ServiceProvider
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Booking, ServiceProvider



class FullBookingForm(forms.ModelForm):
    provider_name = forms.CharField(max_length=100, label="Provider Name")
    service_type = forms.ChoiceField(choices=ServiceProvider.SERVICE_TYPES)
    location = forms.CharField(max_length=100)
    certification = forms.FileField(required=False)
    booking_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Booking
        fields = ['booking_date']

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
