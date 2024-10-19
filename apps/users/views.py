from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserProfileCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserProfileCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Faz login automático após o cadastro
            # Redireciona para a página inicial ou outra de sua escolha
            return redirect('home')
    else:
        form = UserProfileCreationForm()

    return render(request, 'users/register.html', {'form': form})


