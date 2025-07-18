# services/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.views.generic import ListView, TemplateView
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import ServiceProvider, Booking
from .forms import BookingForm, ProviderRegistrationForm, UploadCertificationForm, UserRegisterForm

# --- Home Page with Visit Tracker --- 
class HomeView(TemplateView):
    template_name = 'services/home.html'

    def get(self, request, *args, **kwargs):
        visits = request.session.get('visits', 0)
        request.session['visits'] = visits + 1
        return render(request, self.template_name, {'visits': visits + 1})


# --- List Providers ---
class ProviderListView(ListView):
    model = ServiceProvider
    template_name = 'services/provider_list.html'
    context_object_name = 'providers'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return ServiceProvider.objects.filter(service_type=query)
        return ServiceProvider.objects.all()


# --- Book a Service ---
@login_required
def book_service(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = request.user
            booking.save()
            return redirect('user_history')
    else:
        form = BookingForm()
    return render(request, 'services/book_service.html', {'form': form})



@login_required
def upload_certification(request):
    if request.method == 'POST':
        form = UploadCertificationForm(request.POST, request.FILES)
        if form.is_valid():
            # Assumes ServiceProvider already exists for this user
            provider = ServiceProvider.objects.get(user=request.user)
            provider.certification = form.cleaned_data['certification']
            provider.save()
            return redirect('home')
    else:
        form = UploadCertificationForm()
    return render(request, 'services/upload_cert.html', {'form': form})





@login_required
def user_history(request):
    bookings = Booking.objects.filter(customer=request.user)
    visits = request.session.get('visits', 0)
    return render(request, 'services/user_history.html', {'bookings': bookings, 'visits': visits})



def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'services/register.html', {'form': form})

