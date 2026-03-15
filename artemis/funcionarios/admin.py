from django.contrib import admin
from .models import Funcionarios, Controlo, Equipas, FDocuments, MembrosEquipas

# Register your models here.

@admin.register(Funcionarios)
class FuncionariosAdmin(admin.ModelAdmin):
    # 1. Campos que vão aparecer na lista (tabela) principal de funcionários
    list_display = ('f_id', 'f_nome', 'cargo', 'estado', 'contacto', 'ativo')
    
    # 2. Campos que podem ser pesquisados na barra de busca
    search_fields = ('f_nome', 'contacto', 'conta_bancaria', 'f_id')
    
    # 3. Filtros laterais para facilitar a navegação
    list_filter = ('estado', 'ativo', 'sexo', 'estado_civil')
    
    # 4. Organização visual dos campos na tela de CADASTRO e EDIÇÃO
    fieldsets = (
        ('Informações Pessoais', {
            'fields': ('f_nome', 'naturalidade', 'nacionalidade', 'sexo', 'estado_civil')
        }),
        ('Contactos', {
            'fields': ('contacto', 'contacto_alt')
        }),
        ('Informações Corporativas', {
            'fields': ('cargo', 'departamento', 'estado', 'ativo', 'id_docs', 'id_controlo')
        }),
        ('Informações Bancárias', {
            'fields': ('banco_nome', 'conta_bancaria')
        }),
        ('Outros', {
            'fields': ('avaliacao',)
        }),
    )



admin.site.register(Controlo)
admin.site.register(FDocuments)
admin.site.register(Equipas, list_display = ['nome_equipa','responsavel_equipa','departamento','tipo_equipa','data_inicio','data_fim'])
admin.site.register(MembrosEquipas, list_display = ['f','id_equipas', 'papel'])