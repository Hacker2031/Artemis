from django.db import models
from django.contrib.auth.models import AbstractUser


class Users(AbstractUser):

    TIPO_CHOICES = [
        ('rh',          'Recursos Humanos'),
        ('vendas',      'Vendas'),
        ('stock',       'Stock'),
        ('gestor',      'Gestor'),
        ('admin',      'Admin'),
        ('Programador', 'Programador'),
    ]

    NIVEL_CHOICES = [
        ('operario',    'Operário'),
        ('supervisor',  'Supervisor'),
    ]

    f_id = models.OneToOneField(
        'funcionarios.Funcionarios',
        models.DO_NOTHING,
        db_column='f_id',
        blank=True,
        null=True,
    )

    # Sector/app em que o utilizador trabalha
    tipo = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        default='rh',
        verbose_name='Tipo / Sector',
    )

    # Nível de acesso dentro do sector
    nivel = models.CharField(
        max_length=20,
        choices=NIVEL_CHOICES,
        default='operario',
        verbose_name='Nível',
    )

    # ── helpers de permissão ──────────────────────────────────────────────────

    @property
    def is_programador(self):
        return self.tipo == 'programador'

    @property
    def is_gestor(self):
        """Gestores e programadores vêem o dashboard."""
        return self.tipo in ('gestor', 'programador')

    @property
    def can_access_rh(self):
        """RH e programador acedem à app de funcionários."""
        return self.tipo in ('rh', 'programador')

    @property
    def can_edit_funcionarios(self):
        """Só supervisores (e programador) podem editar/eliminar funcionários."""
        return self.tipo == 'programador' or (
            self.tipo == 'rh' and self.nivel == 'supervisor'
        )

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username
