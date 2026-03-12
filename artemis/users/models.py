from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Users(AbstractUser):
    f_id = models.OneToOneField('funcionarios.Funcionarios', models.DO_NOTHING, db_column='f_id', blank = True, null = True)

    class Meta:
        db_table= 'users'

    def __str__(self):
        return self.username
