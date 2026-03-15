from django.contrib import admin
from .models import Cargos, Departamentos, Vaga, Candidatos, ProcessoSeletivo

# Register your models here.
@admin.register(Vaga)
class VagaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'departamento', 'cargo', 'estado', 'num_vagas', 'data_abertura']
    list_filter = ['estado', 'tipo', 'departamento']
    search_fields = ['titulo']

@admin.register(Candidatos)
class CandidatoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'email', 'vaga', 'estado', 'data_candidatura']
    list_filter = ['estado', 'vaga']
    search_fields = ['nome', 'email']

@admin.register(ProcessoSeletivo)
class ProcessoSeletivoAdmin(admin.ModelAdmin):
    list_display = ['candidato', 'etapa', 'resultado', 'data_agendada', 'avaliador']
    list_filter = ['etapa', 'resultado']
