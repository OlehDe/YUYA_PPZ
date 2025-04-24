from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Event, Comment
from .forms import UserRegistrationForm, EventForm, CommentForm, AdminUserPasswordChangeForm, UserLoginForm


def logout_view(request):
    logout(request)
    return redirect('http://127.0.0.1:8000/')

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('event_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'discussion/register.html', {'form': form})

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

def event_list(request):
    events = Event.objects.all()
    return render(request, 'discussion/event_list.html', {'events': events})

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    comments = event.comments.all()
    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.event = event
            comment.author = request.user
            comment.save()
            return redirect('event_detail', pk=event.pk)
    else:
        form = CommentForm()
    return render(request, 'discussion/event_detail.html', {
        'event': event,
        'comments': comments,
        'form': form
    })

@login_required
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.creator = request.user
            event.save()
            return redirect('event_detail', pk=event.pk)
    else:
        form = EventForm()
    return render(request, 'discussion/event_form.html', {'form': form})

@login_required
def event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.user != event.creator and not request.user.is_staff:
        messages.error(request, 'У вас немає прав для редагування цієї події')
        return redirect('event_detail', pk=event.pk)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            event = form.save()
            return redirect('event_detail', pk=event.pk)
    else:
        form = EventForm(instance=event)
    return render(request, 'discussion/event_form.html', {'form': form})

@login_required
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.user != event.creator and not request.user.is_staff:
        messages.error(request, 'У вас немає прав для видалення цієї події')
        return redirect('event_detail', pk=event.pk)
    if request.method == 'POST':
        event.delete()
        return redirect('event_list')
    return render(request, 'discussion/event_confirm_delete.html', {'event': event})

@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user != comment.author and not request.user.is_staff:
        messages.error(request, 'У вас немає прав для видалення цього коментаря')
        return redirect('event_detail', pk=comment.event.pk)
    if request.method == 'POST':
        event_pk = comment.event.pk
        comment.delete()
        return redirect('event_detail', pk=event_pk)
    return render(request, 'discussion/comment_confirm_delete.html', {'comment': comment})

@user_passes_test(lambda u: u.is_staff)
def admin_user_list(request):
    users = User.objects.all()
    return render(request, 'discussion/user_list.html', {'users': users})

@user_passes_test(lambda u: u.is_staff)
def admin_change_password(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = AdminUserPasswordChangeForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['password1'] == form.cleaned_data['password2']:
                user.set_password(form.cleaned_data['password1'])
                user.save()
                messages.success(request, 'Пароль успішно змінено')
                return redirect('admin_user_list')
            else:
                messages.error(request, 'Паролі не співпадають')
    else:
        form = AdminUserPasswordChangeForm()
    return render(request, 'discussion/change_password.html', {'form': form, 'user': user})