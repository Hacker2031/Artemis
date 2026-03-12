from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Users

# Register your models here.

class CustomUserAdmin(UserAdmin):
    # 1. Adiciona o campo f_id na tela de EDIÇÃO 
    fieldsets = UserAdmin.fieldsets + (
        ('Informações do Funcionário', {
            'fields': ('f_id',),
        }),
    )

    # 2. Adiciona o campo f_id na tela de CRIAÇÃO 
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informações do Funcionário', {
            'fields': ('f_id',),
        }),
    )


admin.site.register(Users, CustomUserAdmin)