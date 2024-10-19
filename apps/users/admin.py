from django.contrib import admin
from apps.users.models import UserProfile

# Register your models here.

@admin.register(UserProfile)
class UsuarioAdmin(admin.ModelAdmin):
    readonly_fields = ("email", "password", "document")


