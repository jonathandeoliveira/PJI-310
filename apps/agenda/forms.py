from django import forms
from .models import Agenda
from apps.users.models import UserProfile
from django.utils import timezone
from django.core.exceptions import ValidationError


class AgendaForm(forms.ModelForm):
    class Meta:
        model = Agenda
        fields = ['professor', 'aluno', 'valor', 'data', 'hora', 'descricao']

        # Customização de widgets para os campos de data e hora
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d'),
            'hora': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={
                'rows': 8, 'cols': 40, 'class': 'form-control',
                'placeholder': 'Exemplo:\n Treino A - Peito:\n - Supino Inclinado 4X10\n - Crucifixo Inclinado 4X10\n - Supino Reto 4X10'
            }),
        }

        # Personaliza os rótulos dos campos do formulário
        labels = {
            'professor': 'Nome do Professor(a)',
            'aluno': 'Nome do Aluno(a)',
            'valor': 'Valor do Treino',
            'data': 'Data do Treino',
            'hora': 'Horário do Treino',
            'descricao': 'Descrição do Treino',
        }

        # Define mensagens de erro personalizadas para cada campo
        error_messages = {
            'professor': {
                'required': 'O nome do professor é obrigatório.',
            },
            'aluno': {
                'required': 'O nome do aluno é obrigatório.',
            },
            'valor': {
                'required': 'O valor do treino é obrigatório.',
                'invalid': 'Insira um valor válido.',
            },
            'data': {
                'required': 'A data do treino é obrigatória.',
            },
            'hora': {
                'required': 'A hora do treino é obrigatória.',
            },
            'descricao': {
                'required': 'A descrição do treino é obrigatória.',
            },
        }
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filtra o campo 'professor' para exibir apenas os usuários com `is_professor=True`
        self.fields['professor'].queryset = UserProfile.objects.filter(is_professor=True)
        
        # Filtra o campo 'aluno' para exibir apenas os usuários com `is_professor=False`
        self.fields['aluno'].queryset = UserProfile.objects.filter(is_professor=False)

    # Validação customizada para garantir que o valor seja positivo
    def clean_valor(self):
        valor = self.cleaned_data.get('valor')
        if valor <= 0:
            raise forms.ValidationError(
                'O valor da aula deve ser maior que zero.')
        return valor

    # Validação customizada para garantir que a data não seja no passado
    def clean_data(self):
        data = self.cleaned_data.get('data')
        if data and data < timezone.now().date():
            raise forms.ValidationError('A data do treino não pode ser no passado.')
        return data

    def clean_aluno_e_professor(self):
        cleaned_data = super().clean()
        professor = cleaned_data.get('professor')
        aluno = cleaned_data.get('aluno')

        # Valida se o professor realmente é um professor
        if professor and not professor.is_professor:
            raise ValidationError("O usuário atribuído como professor não é marcado como professor.")

        # Valida se o aluno não é um professor (caso aluno seja uma ForeignKey para UserProfile)
        if aluno and aluno.is_professor:
            raise ValidationError("O usuário atribuído como aluno é marcado como professor.")
        return cleaned_data