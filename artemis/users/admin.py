from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Users

class CustomUserAdmin(UserAdmin):
    # 1. Adiciona os campos na tela de EDIÇÃO
    fieldsets = UserAdmin.fieldsets + (
        ('Informações de Acesso e Cargo', {
            'fields': ('f_id', 'tipo', 'nivel'),
        }),
    )

    # 2. Adiciona os campos na tela de CRIAÇÃO
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informações de Acesso e Cargo', {
            'fields': ('f_id', 'tipo', 'nivel'),
        }),
    )
    
    # Exibe os campos na lista de usuários do admin
    list_display = ['username', 'email', 'tipo', 'nivel', 'is_staff']
    list_filter = ['tipo', 'nivel', 'is_staff']

admin.site.register(Users, CustomUserAdmin)