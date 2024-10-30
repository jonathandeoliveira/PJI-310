from django.shortcuts import render, redirect
from django.contrib.auth import login
from apps.users.forms import UserProfileCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LoginView
from .forms import UserProfileLoginForm
from django.urls import reverse_lazy

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserProfileCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Faz login automático após o cadastro
            # Redireciona para a página inicial ou outra de sua escolha
            return redirect('index')
    else:
        form = UserProfileCreationForm()
    return render(request, 'users/register.html', {'form': form})


class CustomLoginView(LoginView):
    form_class = UserProfileLoginForm
    template_name = 'users/login.html'

    def get_success_url(self):
        # Redireciona para o nome da URL 'index' após o login
        return reverse_lazy('index')
