from django.db import models

# Create your models here.

class Controlo(models.Model):
    id_controlo = models.AutoField(primary_key=True)
    numero_faltas = models.IntegerField()
    numero_presencas = models.IntegerField()
    inicio_carreira = models.DateField()
    fim_carreira = models.DateField()
    dias_acomulados = models.IntegerField()
    dias_disponiveis = models.IntegerField()
    dias_ferias = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'controlo'




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


class FDocuments(models.Model):
    id_docs = models.AutoField(primary_key=True)
    bi = models.CharField(unique=True, max_length=255)
    passaporte = models.CharField(unique=True, max_length=255, blank=True, null=True)
    atestado = models.CharField(unique=True, max_length=255, blank=True, null=True)
    certificado = models.CharField(unique=True, max_length=255, blank=True, null=True)
    contracto = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'f_documents'


class Funcionarios(models.Model):
    f_id = models.AutoField(primary_key=True)
    f_nome = models.CharField(max_length=45)
    cargo = models.ForeignKey('rh.Cargos', models.DO_NOTHING, db_column='cargo', blank=True, null=True)
    id_docs = models.IntegerField(unique=True, blank=True, null=True)
    estado = models.CharField(max_length=45)
    avaliacao = models.TextField(blank=True, null=True)
    id_controlo = models.OneToOneField(Controlo, models.DO_NOTHING, db_column='id_controlo', blank=True, null=True)
    contacto = models.CharField(unique=True, max_length=25)
    contacto_alt = models.CharField(max_length=45, blank=True, null=True)
    naturalidade = models.CharField(max_length=45)
    nacionalidade = models.CharField(max_length=45)
    sexo = models.CharField(max_length=45)
    estado_civil = models.CharField(max_length=45)
    banco_nome = models.CharField(max_length=45)
    conta_bancaria = models.CharField(unique=True, max_length=45)
    departamento = models.ForeignKey('rh.Departamentos', models.DO_NOTHING, blank=True, null=True)
    ativo = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'funcionarios'
    
    def __str__(self):
        return self.f_nome


class MembrosEquipas(models.Model):
    cod_membro = models.IntegerField(primary_key=True)
    id_equipas = models.ForeignKey(Equipas, models.DO_NOTHING, db_column='id_equipas')
    f = models.ForeignKey(Funcionarios, models.DO_NOTHING)
    papel = models.CharField(max_length=45)
    data_entrada = models.DateField()
    data_saida = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'membros_equipas'
