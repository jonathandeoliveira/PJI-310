from django.core.exceptions import ValidationError
from django.db import models
from apps.users.models import UserProfile
# Create your models here.

class Agenda(models.Model):
    professor = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='professor')
    aluno = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='aluno')
    valor = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    data = models.DateField(null=False, blank=False)
    hora = models.TimeField(null=False, blank=False)
    descricao = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # Valida se o professor realmente é um professor
        if not self.professor.is_professor:
            raise ValidationError("O usuário atribuído como professor não é marcado como professor.")

        # Valida se o aluno não é um professor
        if self.aluno.is_professor:
            raise ValidationError("O usuário atribuído como aluno é marcado como professor.")

    def __str__(self):
        return f"{self.professor} - {self.aluno} - {self.data} {self.hora}"

