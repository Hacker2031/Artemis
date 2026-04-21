from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import date
from .models import Funcionarios, Controlo

@receiver(post_save, sender=Funcionarios)
def criar_controlo_funcionario(sender, instance, created, **kwargs):
    """
    Signal que cria automaticamente um registo de Controlo
    quando um novo funcionário é criado
    """
    if created:  # Apenas quando é criado um novo funcionário
        # Verifica se já não existe um registo de controlo
        if not Controlo.objects.filter(fun_id=instance).exists():
            Controlo.objects.create(
                fun_id=instance,
                numero_faltas=0,
                numero_presencas=0,
                inicio_carreira=instance.data_contratacao or date.today(),
                fim_carreira=None,
                dias_acomulados=0,
                dias_disponiveis=22,
                dias_ferias=22,
                direito_ferias_anual=22,
                ferias_gozadas=0,
                ferias_agendadas=0,
                ferias_restantes=22,
                baixa_medica_dias=0,
                licenca_maternidade_dias=0,
                licenca_sem_vencimento_dias=0,
                ferias_vencidas=0,
                ultimo_ano_ferias=date.today().year,
            )
