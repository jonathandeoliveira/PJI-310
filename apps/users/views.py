from django.shortcuts import render, redirect
from django.contrib.auth import login
from apps.users.forms import UserProfileCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LoginView
from apps.users.forms import UserProfileLoginForm
from django.urls import reverse_lazy


def register(request):
    if request.method == 'POST':
        form = UserProfileCreationForm(request.POST, user=request.user)
        if form.is_valid():
            user = form.save()
            return redirect('index')
    else:
        form = UserProfileCreationForm(user=request.user)
    return render(request, 'users/register.html', {'form': form})

def register_professor(request):
    if request.method == 'POST':
        form = UserProfileCreationForm(request.POST, user=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_professor = True  # Define o usuário como professor
            user.save()
            return redirect('index')
    else:
        form = UserProfileCreationForm(user=request.user)
    return render(request, 'users/register_professor.html', {'form': form})


class CustomLoginView(LoginView):
    form_class = UserProfileLoginForm
    template_name = 'users/login.html'

    def get_success_url(self):
        return reverse_lazy('index')


def logout_view(request):
    logout(request)
    return redirect('index')



