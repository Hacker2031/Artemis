from django.db import models

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