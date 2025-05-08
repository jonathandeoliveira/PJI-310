from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import RegexValidator


class UserProfileManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("O e‑mail é obrigatório")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class UserProfile(AbstractUser):
    # Remove o campo username
    username = None

    # Campos personalizados
    postal_code_validator = RegexValidator(
        regex=r"^\d{8}$", message="O CEP deve ter 8 dígitos."
    )
    document_validator = RegexValidator(
        regex=r"^\d{11}$", message="O CPF deve ter 11 dígitos."
    )
    phone_validator = RegexValidator(
        regex=r"^\d{11}$", message="Telefone com DDD, 11 dígitos."
    )

    document = models.CharField(
        max_length=14, validators=[document_validator], unique=True
    )
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=55)
    postal_code = models.CharField(max_length=12, validators=[postal_code_validator])
    phone = models.CharField(max_length=14, validators=[phone_validator])
    birth_date = models.DateField()
    full_address = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

    is_professor = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        Group, related_name="userprofile_groups", blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission, related_name="userprofile_permissions", blank=True
    )

    # Indica que o login será feito por e‑mail
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["document", "birth_date", "full_address", "postal_code", "phone"]

    objects = UserProfileManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
