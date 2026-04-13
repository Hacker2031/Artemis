from django.db import models
from django.conf import settings
import os


class RelatorioAgendado(models.Model):
    PERIODO_CHOICES = [
        ('diario',  'Diário'),
        ('semanal', 'Semanal'),
        ('mensal',  'Mensal'),
        ('anual',   'Anual'),
    ]
    TIPO_CHOICES = [
        ('usuarios',   'Funcionários'),
        ('stock',      'Stock'),
        ('rh',         'RH / Recrutamento'),
        ('financeiro', 'Financeiro'),
        ('vendas',     'Vendas'),
        ('custom',     'Personalizado'),
    ]
    FORMATO_CHOICES = [
        ('csv',  'CSV (Excel)'),
        ('json', 'JSON'),
        ('txt',  'Texto'),
    ]

    nome             = models.CharField(max_length=150)
    tipo             = models.CharField(max_length=20, choices=TIPO_CHOICES, default='custom')
    periodo          = models.CharField(max_length=10, choices=PERIODO_CHOICES, default='mensal')
    formato          = models.CharField(max_length=10, choices=FORMATO_CHOICES, default='csv')
    ativo            = models.BooleanField(default=True)
    criado_por       = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='relatorios_agendados'
    )
    criado_em        = models.DateTimeField(auto_now_add=True)
    atualizado       = models.DateTimeField(auto_now=True)
    proxima_execucao = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name        = 'Relatório Agendado'
        verbose_name_plural = 'Relatórios Agendados'
        ordering            = ['nome']

    def __str__(self):
        return f'{self.nome} ({self.get_periodo_display()})'


class RelatorioGerado(models.Model):
    STATUS_CHOICES = [
        ('processando', 'Processando'),
        ('concluido',   'Concluído'),
        ('erro',        'Erro'),
    ]

    agendamento   = models.ForeignKey(
        RelatorioAgendado,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='execucoes'
    )
    status        = models.CharField(max_length=15, choices=STATUS_CHOICES, default='processando')
    periodo_ref   = models.CharField(max_length=50)
    # Caminho absoluto no disco — sem depender de MEDIA_ROOT
    arquivo_path  = models.CharField(max_length=500, blank=True, default='')
    nome_arquivo  = models.CharField(max_length=255, blank=True, default='')
    mensagem_erro = models.TextField(blank=True)
    gerado_em     = models.DateTimeField(auto_now_add=True)
    concluido_em  = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name        = 'Relatório Gerado'
        verbose_name_plural = 'Relatórios Gerados'
        ordering            = ['-gerado_em']

    def __str__(self):
        nome = self.agendamento.nome if self.agendamento else 'Avulso'
        return f'{nome} — {self.periodo_ref} [{self.get_status_display()}]'

    @property
    def tem_arquivo(self):
        return bool(self.arquivo_path) and os.path.exists(self.arquivo_path)

    @property
    def url_download(self):
        return f'/relatorios/download/{self.pk}/' if self.tem_arquivo else None