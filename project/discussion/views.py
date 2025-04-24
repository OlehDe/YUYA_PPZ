from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from .models import Event, Review
from .forms import EventForm, ReviewForm, RegistrationForm, UserLoginForm
from django.contrib.auth.decorators import login_required

def base_event(request):
    events = Event.objects.all()
    return render(request, 'discussion/base.html', {'events': events})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user =  authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('http://127.0.0.1:8000/')
    else:
        form = UserLoginForm()
    return render(request, 'discussion/login.html', {'form': form})

def register_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('http://127.0.0.1:8000/')
    else:
        form = RegistrationForm()

    return render(request, 'discussion/register.html', {"form": form})


@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            return redirect('http://127.0.0.1:8000/')
    else:
        form = EventForm()
    return render(request, 'event_form.html', {'form': form})

@login_required
def event_details(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    reviews = event.reviews.all()
    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.event = event
            review.user = request.user
            review.save()
            return redirect('event_details', event_id=event.id)
    else:
        review_form = ReviewForm()
    return render(request, 'event_details.html', {'event': event, 'reviews': reviews, 'review_form': review_form})