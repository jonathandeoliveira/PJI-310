from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile


class UserProfileCreationForm(UserCreationForm):
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'document',
                  'postal_code', 'phone', 'birth_date', 'full_address']

        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Ex.: joaosilva', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'seuemail@exemplo.com', 'class': 'form-control'}),
            'document': forms.TextInput(attrs={'placeholder': 'Digite seu CPF (somente números)', 'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'placeholder': 'Digite seu CEP (somente números)', 'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Digite seu telefone com DDD', 'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'full_address': forms.TextInput(attrs={'placeholder': 'Rua, número, bairro, cidade, estado', 'class': 'form-control'}),
        }

        labels = {
            'username': 'Nome de Usuário',
            'email': 'E-mail',
            'document': 'CPF',
            'postal_code': 'CEP',
            'phone': 'Telefone',
            'birth_date': 'Data de Nascimento',
            'full_address': 'Endereço Completo',
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if UserProfile.objects.filter(email=email).exists():
            raise forms.ValidationError("Este e-mail já está em uso.")
        return email

    def clean_document(self):
        document = self.cleaned_data.get('document')
        if not document.isdigit() or len(document) != 11:
            raise forms.ValidationError(
                "O CPF deve ter exatamente 11 dígitos numéricos.")
        if UserProfile.objects.filter(document=document).exists():
            raise forms.ValidationError("Este CPF já está cadastrado.")
        return document

    def clean_postal_code(self):
        postal_code = self.cleaned_data.get('postal_code')
        if not postal_code.isdigit() or len(postal_code) != 8:
            raise forms.ValidationError(
                "O CEP deve ter exatamente 8 dígitos numéricos.")
        return postal_code

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.isdigit() or len(phone) != 11:
            raise forms.ValidationError(
                "O telefone deve ter exatamente 11 dígitos, incluindo o DDD.")
        return phone
