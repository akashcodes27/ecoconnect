# services/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.views.generic import ListView, TemplateView
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import ServiceProvider, Booking
from .forms import BookingForm, ProviderRegistrationForm, UserRegisterForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404


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


# --- View User Booking History ---
@login_required
def user_history(request):
    bookings = Booking.objects.filter(customer=request.user)
    visits = request.session.get('visits', 0)
    return render(request, 'services/user_history.html', {'bookings': bookings, 'visits': visits})


# --- Register New User ---
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


# --- Login View (handles next redirect) ---
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect(request.POST.get('next') or 'home')
    return render(request, 'services/login.html')


# --- Create a Provider Profile ---
@login_required
def create_provider(request):
    # if ServiceProvider.objects.filter(user=request.user).exists():
    #     return redirect('home')

    if request.method == 'POST':
        form = ProviderRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            provider = form.save(commit=False)
            provider.user = request.user
            provider.save()
            return redirect('providers')
    else:
        form = ProviderRegistrationForm()

    return render(request, 'services/create_provider.html', {'form': form})





@login_required
def provider_dashboard(request):
    providers = ServiceProvider.objects.filter(user=request.user)
    return render(request, 'services/provider_dashboard.html', {'providers': providers})

def about_page(request):
    return render(request, 'services/about.html')

def contact_page(request):
    return render(request, 'services/contact.html')
