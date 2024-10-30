from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import RegexValidator

class UserProfile(AbstractUser):
    # Validadores personalizados
    postal_code_validator = RegexValidator(regex=r'^\d{8}$', message='O CEP deve ter 8 dígitos, exemplo: 12345678.')
    document_validator = RegexValidator(regex=r'^\d{11}$', message='O CPF deve ter 11 dígitos, exemplo: 19876543210.')
    phone_validator = RegexValidator(regex=r'^\d{11}$', message='Insira o telefone com o DDD, exemplo: 11912341234.')

    # Campos personalizados
    document = models.CharField(max_length=14, validators=[document_validator], unique=True)
    postal_code = models.CharField(max_length=12, validators=[postal_code_validator])
    phone = models.CharField(max_length=14, validators=[phone_validator])
    birth_date = models.DateField()
    full_address = models.CharField(max_length=255)
    email = models.EmailField(unique=True, blank=True)

    # Campos específicos para professores
    # Define se o usuário é um professor
    is_professor = models.BooleanField(default=False)
    # Campo de especialidade do professor
    area_atuacao = models.CharField(max_length=50, blank=True, null=True)
  

    # Campos de permissões e grupos
    groups = models.ManyToManyField(Group, related_name='userprofile_groups', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='userprofile_permissions', blank=True)

    REQUIRED_FIELDS = ['document', 'birth_date', 'full_address', 'postal_code', 'phone']
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
