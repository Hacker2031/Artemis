from django.db import models
import datetime
# Create your models here.

class Departamentos(models.Model):
    id_dpt = models.AutoField(primary_key=True)
    nome_dpt = models.CharField(unique=True, max_length=45)
    descricao_dpt = models.TextField()
    dpt_pai = models.ForeignKey('self', models.DO_NOTHING, db_column='dpt_pai', blank=True, null=True)
    responsavel_id = models.IntegerField(blank=True, null=True)
    ativo = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'departamentos'
    
    def __str__(self):
        return self.nome_dpt

class Cargos(models.Model):
    id_cargo = models.AutoField(primary_key=True)
    nome_cargo = models.CharField(max_length=45)
    descricao = models.TextField()
    requisitos = models.TextField()
    sal_min = models.DecimalField(max_digits=10, decimal_places=2)
    sal_base = models.DecimalField(max_digits=10, decimal_places=2)
    sal_max = models.DecimalField(max_digits=10, decimal_places=2)
    data_criacao = models.DateTimeField()
    ativo = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'cargos'

    def __str__(self):
        return self.nome_cargo
    

#Vagas

class Vaga(models.Model):
    cargo = models.ForeignKey(Cargos, on_delete=models.PROTECT, related_name='vagas')
    departamento = models.ForeignKey(Departamentos, on_delete=models.PROTECT, related_name='vagas')
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    requisitos = models.TextField()
    num_vagas = models.PositiveIntegerField(default=1)
    num_candidaturas = models.PositiveIntegerField(default=1)
    salario_oferecido = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    TIPO_CHOICES = [
        ('interno', 'Interno'),
        ('externo', 'Externo'),
        ('misto', 'Interno e Externo'),
    ]

    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='externo')
    
    ESTADO_CHOICES = [
        ('aberta', 'Aberta'),
        ('em_analise', 'Em Análise'),
        ('suspensa', 'Suspensa'),
        ('encerrada', 'Encerrada'),
    ]
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='aberta')

    data_abertura = models.DateField(default=datetime.date.today)
    data_limite = models.DateField(null=True, blank=True)

    data_limite = models.DateField(null=True, blank=True)
    criado_por = models.ForeignKey('users.Users', on_delete=models.SET_NULL, null=True)
    
    class Meta:
        managed = False
        db_table = 'vagas'
        verbose_name = 'Vaga'
        verbose_name_plural = 'Vagas'

    def __str__(self):
        return f"{self.titulo} ({self.get_estado_display()})"
    
#Candidatos às referidas vagas
class Candidatos(models.Model):
    nome = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=9)
    nacionalidade = models.CharField(max_length=45, default='angolana')

    #CV. Aprendi este código para guardar ficheiros. Usar no FDocuments. Não esquece Gililson. Por favor. Não esquece. E agora estou a falar sozinho nos comentários. Patético.

    cv = models.FileField(upload_to='candidatos/cvs', null=True, blank=True)

    vaga = models.ForeignKey(Vaga, on_delete=models.CASCADE, related_name='candidatos')
    nota = models.TextField()

    ESTADO_CHOICES = [
        ('recebido', 'Recebido'),
        ('em_analise', 'Em Análise'),
        ('entrevista', 'Convocado para Entrevista'),
        ('teste', 'Em Teste'),
        ('oferta', 'Oferta Enviada'),
        ('contratado', 'Contratado'),
        ('rejeitado', 'Rejeitado'),
    ]
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='recebido')
    
    data_candidatura = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'candidatos'
        verbose_name = 'Candidato'
        verbose_name_plural = 'Candidatos'

    def __str__(self):
        return f"{self.nome} -> {self.vaga.titulo}"
    
class ProcessoSeletivo(models.Model):
    candidato = models.ForeignKey(Candidatos, on_delete=models.CASCADE, related_name='processos')

    ETAPA_CHOICES = [
        ('entrevista_rh', 'Entrevista RH'),
        ('entrevista_tecnica', 'Entrevista Técnica'),
        ('teste_escrito', 'Teste Escrito'),
        ('teste_pratico', 'Teste Prático'),
        ('proposta', 'Proposta/Oferta'),
    ]
    etapa = models.CharField(max_length=30, choices=ETAPA_CHOICES)

    RESULTADO_CHOICES = [
        ('pendente', 'Pendente'),
        ('aprovado', 'Aprovado'),
        ('reprovado', 'Reprovado'),
    ]
    resultado = models.CharField(max_length=20, choices=RESULTADO_CHOICES, default='pendente')

    data_agendada = models.DateTimeField(null=True, blank=True)

    # Quem do nosso lado faz a entrevista/avaliação

    avaliador = models.ForeignKey(
        'funcionarios.Funcionarios', 
        on_delete=models.SET_NULL, 
        null=True, blank=True
    )
    nota = models.IntegerField(default=1)
    observacoes = models.TextField(blank=True, null=True)
    data_registo = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'processo_seletivo'
        verbose_name = 'Processo Seletivo'
        verbose_name_plural = 'Processos Seletivos'

    def __str__(self):
        return f"{self.candidatos.nome} | {self.get_etapa_display()} — {self.get_resultado_display()}"