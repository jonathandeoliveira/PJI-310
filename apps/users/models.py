from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import RegexValidator
from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("O email é obrigatório")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superusuário precisa ter is_staff=True")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superusuário precisa ter is_superuser=True")

        return self.create_user(email, password, **extra_fields)


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
    email = models.EmailField(unique=True, blank=False)

    # Campos específicos para professores
    # Define se o usuário é um professor
    is_professor = models.BooleanField(default=False)

    # Campos de permissões e grupos
    groups = models.ManyToManyField(Group, related_name='userprofile_groups', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='userprofile_permissions', blank=True)

    REQUIRED_FIELDS = ['document', 'birth_date', 'full_address', 'postal_code', 'phone']
    USERNAME_FIELD = 'email'
    
    objects = CustomUserManager()


    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

