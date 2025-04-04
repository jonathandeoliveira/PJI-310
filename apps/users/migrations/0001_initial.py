# Generated by Django 5.1.1 on 2025-03-31 21:56

import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                (
                    "document",
                    models.CharField(
                        max_length=14,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="O CPF deve ter 11 dígitos, exemplo: 19876543210.",
                                regex="^\\d{11}$",
                            )
                        ],
                    ),
                ),
                (
                    "postal_code",
                    models.CharField(
                        max_length=12,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="O CEP deve ter 8 dígitos, exemplo: 12345678.",
                                regex="^\\d{8}$",
                            )
                        ],
                    ),
                ),
                (
                    "phone",
                    models.CharField(
                        max_length=14,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Insira o telefone com o DDD, exemplo: 11912341234.",
                                regex="^\\d{11}$",
                            )
                        ],
                    ),
                ),
                ("birth_date", models.DateField()),
                ("full_address", models.CharField(max_length=255)),
                ("email", models.EmailField(blank=True, max_length=254, unique=True)),
                ("is_professor", models.BooleanField(default=False)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True, related_name="userprofile_groups", to="auth.group"
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        related_name="userprofile_permissions",
                        to="auth.permission",
                    ),
                ),
            ],
            options={
                "verbose_name": "User Profile",
                "verbose_name_plural": "User Profiles",
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
