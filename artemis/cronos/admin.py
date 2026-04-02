from django.contrib import admin
from .models import ConversaCronos, MensagemCronos


@admin.register(ConversaCronos)
class ConversaCronosAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'titulo', 'data_inicio', 'num_mensagens', 'ativa')
    list_filter = ('ativa', 'data_inicio', 'usuario')
    search_fields = ('usuario__username', 'titulo', 'resumo')
    readonly_fields = ('data_inicio', 'data_fim', 'num_mensagens')
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('usuario', 'titulo', 'ativa')
        }),
        ('Conteúdo', {
            'fields': ('resumo',)
        }),
        ('Timestamps', {
            'fields': ('data_inicio', 'data_fim', 'num_mensagens'),
            'classes': ('collapse',)
        }),
    )


@admin.register(MensagemCronos)
class MensagemCronosAdmin(admin.ModelAdmin):
    list_display = ('conversa', 'tipo', 'tipo_resposta', 'data_criacao', 'tokens_utilizados')
    list_filter = ('tipo', 'tipo_resposta', 'data_criacao', 'conversa__usuario')
    search_fields = ('conversa__usuario__username', 'conteudo')
    readonly_fields = ('data_criacao',)
    fieldsets = (
        ('Mensagem', {
            'fields': ('conversa', 'tipo', 'conteudo')
        }),
        ('Resposta', {
            'fields': ('tipo_resposta', 'sql_gerado', 'resultado_sql'),
            'classes': ('collapse',)
        }),
        ('Metadados', {
            'fields': ('data_criacao', 'tokens_utilizados'),
            'classes': ('collapse',)
        }),
    )
