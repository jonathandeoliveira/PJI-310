from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserProfile


class UserProfileCreationForm(UserCreationForm):
    class Meta:
        model = UserProfile
        fields = [
            'username',
            'email',
            'document',
            'postal_code',
            'phone',
            'birth_date',
            'full_address',
            'is_professor',
            'area_atuacao',
            
        ]

        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Ex.: Joaosilva', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Joaosilva@exemplo.com', 'class': 'form-control'}),
            'document': forms.TextInput(attrs={'placeholder': 'Digite seu CPF (somente números)', 'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'placeholder': 'Digite seu CEP (somente números)', 'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Digite seu telefone com DDD', 'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'full_address': forms.TextInput(attrs={'placeholder': 'Rua, Número, Bairro, Cidade, Estado', 'class': 'form-control'}),
            'is_professor': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'area_atuacao': forms.TextInput(attrs={'placeholder': 'Área de Atuação do Professor', 'class': 'form-control'}),
            
        }

        labels = {
            'username': 'Nome de Usuário',
            'email': 'E-mail',
            'document': 'CPF',
            'postal_code': 'CEP',
            'phone': 'Telefone',
            'birth_date': 'Data de Nascimento',
            'full_address': 'Endereço Completo',
            'area_atuacao': 'Área de Atuação',
            'is_professor': 'É Professor?',
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


class UserProfileLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="E-mail",
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Digite seu E-mail'})
    )
    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Senha'})
    )
