from django.db import models

# Create your models here.

class Agenda(models.Model):
    professor = models.CharField(max_length=100, null=False, blank=False)
    aluno = models.CharField(max_length=100, null=False, blank=False)
    valor = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    data = models.DateField(null=False, blank=False)
    hora = models.TimeField(null=False, blank=False)
    descricao = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.professor} - {self.aluno} - {self.data} {self.hora}"

