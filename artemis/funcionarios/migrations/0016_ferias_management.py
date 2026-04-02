# Generated migration for ferias management

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('funcionarios', '0015_controlo_fun_id_fdocuments_fun_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='controlo',
            name='direito_ferias_anual',
            field=models.IntegerField(default=22, help_text='Dias de férias anuais por lei'),
        ),
        migrations.AddField(
            model_name='controlo',
            name='ferias_gozadas',
            field=models.IntegerField(default=0, help_text='Dias de férias já tirados'),
        ),
        migrations.AddField(
            model_name='controlo',
            name='ferias_agendadas',
            field=models.IntegerField(default=0, help_text='Dias de férias marcadas'),
        ),
        migrations.AddField(
            model_name='controlo',
            name='ferias_restantes',
            field=models.IntegerField(default=22, help_text='Dias restantes (calculado)'),
        ),
        migrations.AddField(
            model_name='controlo',
            name='baixa_medica_dias',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='controlo',
            name='licenca_maternidade_dias',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='controlo',
            name='licenca_sem_vencimento_dias',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='controlo',
            name='ferias_vencidas',
            field=models.IntegerField(default=0, help_text='Dias que expiraram sem gozar'),
        ),
        migrations.AddField(
            model_name='controlo',
            name='ultimo_ano_ferias',
            field=models.IntegerField(default=0, help_text='Ano da última atualização de férias'),
        ),
        migrations.AlterField(
            model_name='controlo',
            name='dias_acomulados',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='controlo',
            name='dias_disponiveis',
            field=models.IntegerField(default=22),
        ),
        migrations.AlterField(
            model_name='controlo',
            name='dias_ferias',
            field=models.IntegerField(default=22),
        ),
        migrations.AlterField(
            model_name='controlo',
            name='fim_carreira',
            field=models.DateField(blank=True, null=True),
        ),
    ]
