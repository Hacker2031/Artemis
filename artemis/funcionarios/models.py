from django.db import models
from rh.models import Candidatos
# Create your models here.

class Controlo(models.Model):
    id_controlo = models.AutoField(primary_key=True)
    fun_id = models.ForeignKey('Funcionarios', models.DO_NOTHING, db_column='f_id', blank=True, null=True) 
    numero_faltas = models.IntegerField()
    numero_presencas = models.IntegerField()
    inicio_carreira = models.DateField()
    fim_carreira = models.DateField(blank=True, null=True)
    dias_acomulados = models.IntegerField(default=0)
    dias_disponiveis = models.IntegerField(default=22)
    dias_ferias = models.IntegerField(default=22)
    
    # Campos para planeamento de férias
    direito_ferias_anual = models.IntegerField(default=22, help_text="Dias de férias anuais por lei")
    ferias_gozadas = models.IntegerField(default=0, help_text="Dias de férias já tirados")
    ferias_agendadas = models.IntegerField(default=0, help_text="Dias de férias marcadas")
    ferias_restantes = models.IntegerField(default=22, help_text="Dias restantes (calculado)")
    
    # Outros tipos de ausência
    baixa_medica_dias = models.IntegerField(default=0)
    licenca_maternidade_dias = models.IntegerField(default=0)
    licenca_sem_vencimento_dias = models.IntegerField(default=0)
    
    # Histórico
    ferias_vencidas = models.IntegerField(default=0, help_text="Dias que expiraram sem gozar")
    ultimo_ano_ferias = models.IntegerField(default=0, help_text="Ano da última atualização de férias")

    class Meta:
        managed = True
        db_table = 'controlo'
    
    def __str__(self):
        func = self.fun_id.f_nome if self.fun_id else "N/A"
        return f"Controlo - {func}"




class Equipas(models.Model):
    id_equipas = models.AutoField(primary_key=True)
    nome_equipa = models.CharField(unique=True, max_length=45)
    responsavel_equipa = models.ForeignKey('Funcionarios', models.DO_NOTHING, db_column='responsavel_equipa', blank=True, null=True)
    departamento = models.ForeignKey('rh.Departamentos', models.DO_NOTHING, blank=True, null=True)
    data_inicio = models.DateField()
    data_fim = models.DateField(blank=True, null=True)
    ativo = models.IntegerField()
    tipo_equipa = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'equipas'
        verbose_name = 'Equipa'
        verbose_name_plural = 'Equipas'
    def __str__(self):
        return f"{self.nome_equipa}"


class PlanamentFerias(models.Model):
    """Model para planeamento e solicitação de férias"""
    TIPO_AUSENCIA_CHOICES = [
        ('ferias', 'Férias Anuais'),
        ('medica', 'Baixa Médica'),
        ('maternidade', 'Licença Maternidade/Paternidade'),
        ('sem_vencimento', 'Licença sem Vencimento'),
    ]
    
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('aprovado', 'Aprovado'),
        ('rejeitado', 'Rejeitado'),
        ('cancelado', 'Cancelado'),
    ]
    
    id_solicitacao = models.AutoField(primary_key=True)
    funcionario = models.ForeignKey('Funcionarios', on_delete=models.CASCADE, related_name='solicitacoes_ferias')
    tipo_ausencia = models.CharField(max_length=20, choices=TIPO_AUSENCIA_CHOICES, default='ferias')
    data_inicio = models.DateField()
    data_fim = models.DateField()
    dias_uteis = models.IntegerField(default=0, help_text="Número de dias úteis")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    
    observacoes = models.TextField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    aprovado_por = models.ForeignKey('Funcionarios', on_delete=models.SET_NULL, null=True, blank=True, related_name='ferias_aprovadas')
    data_aprovacao = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        managed = True
        db_table = 'planeament_ferias'
        verbose_name = 'Planeamento de Férias'
        verbose_name_plural = 'Planeamentos de Férias'
        ordering = ['-data_inicio']
    
    def __str__(self):
        return f"{self.funcionario.f_nome} - {self.get_tipo_ausencia_display()} ({self.data_inicio})"


class FDocuments(models.Model):
    id_docs = models.AutoField(primary_key=True)
    fun_id = models.ForeignKey('Funcionarios', models.DO_NOTHING, db_column='f_id', blank=True, null=True) 
    bi = models.CharField(unique=True, max_length=255)
    passaporte = models.CharField(unique=True, max_length=255, blank=True, null=True)
    atestado = models.CharField(unique=True, max_length=255, blank=True, null=True)
    certificado = models.CharField(unique=True, max_length=255, blank=True, null=True)
    contracto = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = True
        db_table = 'f_documents'
        verbose_name='Documentos'



class Funcionarios(models.Model):
    ATIVO_CHOICES=[
    ('ativo', 'Ativo'),
    ('ferias', 'Férias'),
    ('afastado', 'Afastado'),
    ('demitido', 'Demitido'),
]
    EVENTUAL_CHOICES=[
    ('efetivo', 'Efetivo'),
    ('em formação', 'Em Formação'),
    ('eventual', 'Eventual'),
]
    f_id = models.AutoField(primary_key=True)
    f_nome = models.CharField(max_length=45)
    cargo = models.ForeignKey('rh.Cargos', on_delete= models.DO_NOTHING, db_column='cargo', blank=True, null=True)
    estado = models.CharField(max_length=45, choices=EVENTUAL_CHOICES, default='efetivo')
    avaliacao = models.FloatField(blank=True, null=True) 
    contacto = models.CharField(unique=True, max_length=25)
    foto_perfil = models.FileField(upload_to="rh/foto_perfil_funcionarios", null=True, blank=True)
    contacto_alt = models.CharField(max_length=45, blank=True, null=True)
    naturalidade = models.CharField(max_length=45, blank=True, null=True)
    nacionalidade = models.CharField(max_length=45, choices=Candidatos.NACIONALIDADE_CHOICES)
    sexo = models.CharField(max_length=45)
    cidade = models.CharField(max_length=45, blank=True, null=True)
    PROVINCIA_CHOICES = [
    ('luanda', 'Luanda'),
    ('bengo', 'Bengo'),
    ('benguela', 'Benguela'),
    ('bie', 'Bié'),
    ('cabinda', 'Cabinda'),
    ('cuando', 'Cuando'),
    ('cubango', 'Cubango'),
    ('cuanza_norte', 'Cuanza Norte'),
    ('cuanza_sul', 'Cuanza Sul'),
    ('cunene', 'Cunene'),
    ('huambo', 'Huambo'),
    ('huila', 'Huíla'),
    ('lunda_norte', 'Lunda Norte'),
    ('lunda_sul', 'Lunda Sul'),
    ('malanje', 'Malanje'),
    ('moxico', 'Moxico'),
    ('moxico_leste', 'Moxico-Leste'),
    ('namibe', 'Namibe'),
    ('icolo_bengo', 'Icolo e Bengo'),
    ('uige', 'Uíge'),
    ('zaire', 'Zaire'),
]
    provincia = models.CharField(max_length=45, choices=PROVINCIA_CHOICES, default="luanda")
    endereco = models.TextField(max_length=120, blank=True, null=True)
    estado_civil = models.CharField(max_length=45)
    num_bi = models.CharField(max_length=45, unique=True, null=True)
    banco_nome = models.CharField(max_length=45)
    conta_bancaria = models.CharField(unique=True, max_length=45)
    departamento = models.ForeignKey('rh.Departamentos', on_delete = models.DO_NOTHING, blank=True, null=True)
    ativo = models.CharField(max_length=15, choices= ATIVO_CHOICES, default='ativo')
    data_contratacao = models.DateField(null=True, blank=True)
    data_nasc = models.DateField(null=True, blank=True)
    data_demissao = models.DateField(null=True, blank=True, help_text="Data de demissão ou desligamento")
    supervisor = models.ForeignKey('self', on_delete = models.DO_NOTHING, blank=True, null=True)
    iban = models.CharField(max_length=45, null=True, blank= True)
    titular = models.CharField(max_length=45, null=True, blank= True)
    
    
    class Meta:
        managed = True
        db_table = 'funcionarios'
        verbose_name='Funcionario'
        verbose_name_plural='Funcionarios'
    
    def __str__(self):
        return f"{self.f_nome} - {self.cargo}"


class MembrosEquipas(models.Model):
    cod_membro = models.AutoField(primary_key=True)
    id_equipas = models.ForeignKey(Equipas, models.DO_NOTHING, db_column='id_equipas')
    f = models.ForeignKey(Funcionarios, models.DO_NOTHING, null=True)
    papel = models.CharField(max_length=45)
    data_entrada = models.DateField()
    data_saida = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'membros_equipas'
        verbose_name='Membro de Equipa'
        verbose_name_plural='Membros de Equipas'
    
