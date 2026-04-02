from django.core.management.base import BaseCommand
from django.utils import timezone
from funcionarios.models import Funcionarios, Controlo
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Popula a tabela Controlo com registos para todos os funcionários que não têm'

    def handle(self, *args, **options):
        funcionarios = Funcionarios.objects.filter(ativo='ativo')
        criados = 0
        atualizados = 0

        for funcionario in funcionarios:
            # Verifica se já existe registo de controlo
            controlo, criado = Controlo.objects.get_or_create(
                fun_id=funcionario,
                defaults={
                    'numero_faltas': 0,
                    'numero_presencas': 0,
                    'inicio_carreira': funcionario.data_contratacao or date.today(),
                    'fim_carreira': None,
                    'dias_acomulados': 0,
                    'dias_disponiveis': 22,
                    'dias_ferias': 22,
                    'direito_ferias_anual': 22,
                    'ferias_gozadas': 0,
                    'ferias_agendadas': 0,
                    'ferias_restantes': 22,
                    'baixa_medica_dias': 0,
                    'licenca_maternidade_dias': 0,
                    'licenca_sem_vencimento_dias': 0,
                    'ferias_vencidas': 0,
                    'ultimo_ano_ferias': date.today().year,
                }
            )

            if criado:
                criados += 1
                self.stdout.write(self.style.SUCCESS(
                    f'✓ Criado registo de controlo para: {funcionario.f_nome}'
                ))
            else:
                atualizados += 1

        self.stdout.write(self.style.SUCCESS(
            f'\n📊 Resumo:'
        ))
        self.stdout.write(self.style.SUCCESS(
            f'   - Novos registos criados: {criados}'
        ))
        self.stdout.write(self.style.WARNING(
            f'   - Registos que já existiam: {atualizados}'
        ))
        self.stdout.write(self.style.SUCCESS(
            f'   - Total de funcionários processados: {criados + atualizados}'
        ))
