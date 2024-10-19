from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile


class UserProfileCreationForm(UserCreationForm):
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'document', 'postal_code', 'phone', 'birth_date', 'full_address']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }

    # Se você quiser adicionar validações personalizadas
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if UserProfile.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email já está em uso.")
        return email
