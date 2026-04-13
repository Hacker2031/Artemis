from django.contrib import admin
from .models import RelatorioAgendado, RelatorioGerado


class RelatorioGeradoInline(admin.TabularInline):
    model  = RelatorioGerado
    extra  = 0
    fields = ('status', 'periodo_ref', 'arquivo_path', 'gerado_em', 'concluido_em')
    readonly_fields = ('status', 'periodo_ref', 'arquivo_path', 'gerado_em', 'concluido_em')



@admin.register(RelatorioAgendado)
class RelatorioAgendadoAdmin(admin.ModelAdmin):
    list_display  = ('nome', 'tipo', 'periodo', 'formato', 'ativo', 'proxima_execucao')
    list_filter   = ('tipo', 'periodo', 'ativo')
    search_fields = ('nome',)
    inlines       = [RelatorioGeradoInline]


@admin.register(RelatorioGerado)
class RelatorioGeradoAdmin(admin.ModelAdmin):
    list_display  = ('agendamento', 'status', 'periodo_ref', 'gerado_em', 'concluido_em')
    list_filter   = ('status',)
    readonly_fields = ('gerado_em', 'concluido_em')