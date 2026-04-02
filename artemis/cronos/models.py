from django.db import models
from users.models import Users


class ConversaCronos(models.Model):
    """Armazena cada conversa (sessão) com o Cronos"""

    usuario = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        related_name='conversas_cronos'
    )
    titulo = models.CharField(
        max_length=200,
        default='Nova Conversa',
        help_text='Título da conversa'
    )
    resumo = models.TextField(
        blank=True,
        null=True,
        help_text='Resumo automático da conversa'
    )
    data_inicio = models.DateTimeField(auto_now_add=True)
    data_fim = models.DateTimeField(
        blank=True,
        null=True,
        help_text='Data de encerramento da conversa'
    )
    ativa = models.BooleanField(
        default=True,
        help_text='Se a conversa está activa'
    )
    num_mensagens = models.IntegerField(
        default=0,
        help_text='Total de mensagens na conversa'
    )

    class Meta:
        db_table = 'cronos_conversas'
        verbose_name = 'Conversa Cronos'
        verbose_name_plural = 'Conversas Cronos'
        ordering = ['-data_inicio']
        indexes = [
            models.Index(fields=['usuario', '-data_inicio']),
            models.Index(fields=['ativa']),
        ]

    def __str__(self):
        return f"{self.usuario.username} - {self.titulo} ({self.data_inicio.strftime('%d/%m/%Y %H:%M')})"


class MensagemCronos(models.Model):
    """Armazena cada mensagem dentro de uma conversa"""

    TIPO_CHOICES = [
        ('user', 'Utilizador'),
        ('assistant', 'Cronos'),
    ]

    RESPOSTA_CHOICES = [
        ('fixa', 'Resposta Fixa'),
        ('sql', 'Com Consulta SQL'),
        ('text', 'Texto Puro'),
    ]

    conversa = models.ForeignKey(
        ConversaCronos,
        on_delete=models.CASCADE,
        related_name='mensagens'
    )
    tipo = models.CharField(
        max_length=10,
        choices=TIPO_CHOICES,
        help_text='Quem enviou a mensagem'
    )
    conteudo = models.TextField(
        help_text='Texto da mensagem'
    )
    tipo_resposta = models.CharField(
        max_length=10,
        choices=RESPOSTA_CHOICES,
        default='text',
        help_text='Tipo de resposta gerada (apenas para tipo=assistant)'
    )
    sql_gerado = models.TextField(
        blank=True,
        null=True,
        help_text='SQL gerado (se aplicável)'
    )
    resultado_sql = models.TextField(
        blank=True,
        null=True,
        help_text='Resultado da execução do SQL'
    )
    data_criacao = models.DateTimeField(auto_now_add=True)
    tokens_utilizados = models.IntegerField(
        default=0,
        help_text='Tokens usados nesta interação (para análise de custos)'
    )

    class Meta:
        db_table = 'cronos_mensagens'
        verbose_name = 'Mensagem Cronos'
        verbose_name_plural = 'Mensagens Cronos'
        ordering = ['data_criacao']
        indexes = [
            models.Index(fields=['conversa', 'data_criacao']),
            models.Index(fields=['tipo']),
        ]

    def __str__(self):
        preview = self.conteudo[:50] + '...' if len(self.conteudo) > 50 else self.conteudo
        return f"[{self.tipo.upper()}] {preview}"
