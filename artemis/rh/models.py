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

    #P.S: pedi à umaa I.A para me gerar um dicionário contendo as 195 possíveis nacionalidades neste mundo(que eu acredito ser plano)
    NACIONALIDADE_CHOICES = [

    # ÁFRICA
    ('angolana', 'Angolana'),
    ('mocambicana', 'Moçambicana'),
    ('caboverdiana', 'Cabo-verdiana'),
    ('guineense', 'Guineense (Guiné-Bissau)'),
    ('santomense', 'Santomense'),
    ('sul_africana', 'Sul-africana'),
    ('nigeriana', 'Nigeriana'),
    ('egipcia', 'Egípcia'),
    ('marroquina', 'Marroquina'),
    ('argelina', 'Argelina'),
    ('tunisia', 'Tunisina'),
    ('libia', 'Líbia'),
    ('sudanesa', 'Sudanesa'),
    ('sul_sudanesa', 'Sul-sudanesa'),
    ('etiopica', 'Etíope'),
    ('eritreia', 'Eritreia'),
    ('somali', 'Somali'),
    ('queniana', 'Queniana'),
    ('tanzaniana', 'Tanzaniana'),
    ('ugandense', 'Ugandense'),
    ('ruandesa', 'Ruandesa'),
    ('burundesa', 'Burundesa'),
    ('congolesa', 'Congolesa (Congo)'),
    ('rd_congolesa', 'Congolesa (RDC)'),
    ('gabonesa', 'Gabonesa'),
    ('camaronesa', 'Camaronesa'),
    ('chadiana', 'Chadiana'),
    ('nigerina', 'Nigerina'),
    ('mali', 'Maliana'),
    ('senegalesa', 'Senegalesa'),
    ('gambiana', 'Gambiana'),
    ('guineense_conacri', 'Guineense (Guiné-Conacri)'),
    ('liberiana', 'Liberiana'),
    ('serra_leonesa', 'Serra-leonesa'),
    ('ganesa', 'Ganesa'),
    ('togolesa', 'Togolesa'),
    ('beninense', 'Beninense'),
    ('zambiana', 'Zambiana'),
    ('zimbabueana', 'Zimbabueana'),
    ('botsuanesa', 'Botsuanesa'),
    ('namibiana', 'Namibiana'),
    ('malgaxe', 'Malgaxe'),
    ('mauriciana', 'Mauriciana'),
    ('seichelense', 'Seichelense'),
    ('comorense', 'Comorense'),

    #  EUROPA
    ('portuguesa', 'Portuguesa'),
    ('espanhola', 'Espanhola'),
    ('francesa', 'Francesa'),
    ('italiana', 'Italiana'),
    ('alemã', 'Alemã'),
    ('holandesa', 'Holandesa'),
    ('belga', 'Belga'),
    ('suica', 'Suíça'),
    ('austriaca', 'Austríaca'),
    ('britanica', 'Britânica'),
    ('irlandesa', 'Irlandesa'),
    ('norueguesa', 'Norueguesa'),
    ('sueca', 'Sueca'),
    ('dinamarquesa', 'Dinamarquesa'),
    ('finlandesa', 'Finlandesa'),
    ('islandesa', 'Islandesa'),
    ('polonesa', 'Polonesa'),
    ('tcheca', 'Tcheca'),
    ('eslovaca', 'Eslovaca'),
    ('hungara', 'Húngara'),
    ('romena', 'Romena'),
    ('bulgara', 'Búlgara'),
    ('grega', 'Grega'),
    ('turca', 'Turca'),
    ('ucraniana', 'Ucraniana'),
    ('russa', 'Russa'),
    ('bielorrussa', 'Bielorrussa'),
    ('lituana', 'Lituana'),
    ('letona', 'Letona'),
    ('estoniana', 'Estoniana'),
    ('croata', 'Croata'),
    ('servia', 'Sérvia'),
    ('bósnia', 'Bósnia'),
    ('eslovena', 'Eslovena'),
    ('albanesa', 'Albanesa'),
    ('macedonia', 'Macedónia'),
    ('montenegrina', 'Montenegrina'),

    # AMÉRICAS
    ('americana', 'Americana'),
    ('canadense', 'Canadense'),
    ('mexicana', 'Mexicana'),
    ('brasileira', 'Brasileira'),
    ('argentina', 'Argentina'),
    ('chilena', 'Chilena'),
    ('colombiana', 'Colombiana'),
    ('peruana', 'Peruana'),
    ('venezuelana', 'Venezuelana'),
    ('equatoriana', 'Equatoriana'),
    ('boliviana', 'Boliviana'),
    ('paraguaia', 'Paraguaia'),
    ('uruguaia', 'Uruguaia'),
    ('cubana', 'Cubana'),
    ('haitiana', 'Haitiana'),
    ('dominicana', 'Dominicana'),
    ('jamaicana', 'Jamaicana'),
    ('trinitina', 'Trinitina'),
    ('barbadense', 'Barbadense'),
    ('costarriquenha', 'Costarriquenha'),
    ('panamenha', 'Panamenha'),
    ('nicaraguense', 'Nicaraguense'),
    ('hondurenha', 'Hondurenha'),
    ('salvadorenha', 'Salvadorenha'),
    ('guatemalteca', 'Guatemalteca'),

    #  ÁSIA
    ('chinesa', 'Chinesa'),
    ('japonesa', 'Japonesa'),
    ('sul_coreana', 'Sul-coreana'),
    ('norte_coreana', 'Norte-coreana'),
    ('indiana', 'Indiana'),
    ('paquistanesa', 'Paquistanesa'),
    ('bangladeshiana', 'Bangladeshiana'),
    ('nepalesa', 'Nepalesa'),
    ('butanesa', 'Butanesa'),
    ('ceilandesa', 'Cingalesa'),
    ('afegã', 'Afegã'),
    ('iraniana', 'Iraniana'),
    ('iraquiana', 'Iraquiana'),
    ('saudita', 'Saudita'),
    ('emiradense', 'Emiratense'),
    ('catarense', 'Catarense'),
    ('kuwaitiana', 'Kuwaitiana'),
    ('omanense', 'Omanense'),
    ('iemenita', 'Iemenita'),
    ('israelense', 'Israelense'),
    ('libanesa', 'Libanesa'),
    ('jordana', 'Jordana'),
    ('siria', 'Síria'),
    ('turcomena', 'Turcomena'),
    ('cazaque', 'Cazaque'),
    ('uzbeque', 'Uzbeque'),
    ('quirguiz', 'Quirguiz'),
    ('tajique', 'Tajique'),
    ('mongol', 'Mongol'),
    ('tailandesa', 'Tailandesa'),
    ('vietnamita', 'Vietnamita'),
    ('laociana', 'Laociana'),
    ('cambojana', 'Cambojana'),
    ('malasia', 'Malaia'),
    ('singapurense', 'Singapurense'),
    ('indonesiana', 'Indonésia'),
    ('filipina', 'Filipina'),

    #  OCEANIA
    ('australiana', 'Australiana'),
    ('neozelandesa', 'Neozelandesa'),
    ('fijiana', 'Fijiana'),
    ('papua', 'Papua-Nova Guiné'),
    ('samoana', 'Samoana'),
    ('tonganesa', 'Tonganesa'),
    ('vanuatuense', 'Vanuatuense'),
    ('micronesia', 'Micronésia'),
    ('kiribatiana', 'Kiribatiana'),
    ('tuvaluana', 'Tuvaluana')

    ]
    nacionalidade = models.CharField(max_length=45,choices=NACIONALIDADE_CHOICES, default='angolana')


    #CV. Aprendi este código para guardar ficheiros. Usar no FDocuments. Não esquece Gililson. Por favor. Não esquece. E agora estou a falar sozinho nos comentários. Patético.
    cv = models.FileField(upload_to='rh/candidatos/cvs', null=True, blank=True)
    FONTE_RECRUTAMENTO_CHOICES = [
        ('linkedin', 'LinkedIN'),
        ('portal_recrutamento', 'Portal de Emprego'),
        ('indicacao_interna', 'Indicação Interna'),
        ('candidatura_livre', 'Candidatura Espontânea'),
        ('outra', 'Outra'),
    ]
    fonte_recrutamento = models.CharField(max_length=69, choices=FONTE_RECRUTAMENTO_CHOICES, default='linkedin')
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