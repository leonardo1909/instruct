from uuid import uuid4
from django.db import models


class Municipio(models.Model):
    codigo = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
        db_column='cd_acesso'
    )
    codigo_ibge = models.CharField(
        max_length=7,
        db_column='nr_codigo_ibge'
    )
    nome = models.CharField(
        max_length=40,
        db_column='nm_municipio'
    )

    class Meta:
        db_table = 'tb_municipio'

    def __str__(self):
        return f'{self.codigo}'


class Estado(models.Model):
    codigo = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
        db_column='cd_acesso'
    )
    codigo_ibge = models.CharField(
        max_length=7,
        db_column='nr_codigo_ibge'
    )
    nome = models.CharField(
        max_length=40,
        db_column='nm_estado'
    )

    class Meta:
        db_table = 'tb_estado'

    def __str__(self):
        return f'{self.codigo}'


class Feriado(models.Model):
    codigo = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
        db_column='cd_acesso'
    )
    municipio = models.ForeignKey(
        Municipio, on_delete=models.DO_NOTHING,
        related_name='feriado_municipio',
        related_query_name='feriados_municipios',
        null=True,
        db_column='cd_municipio'
    )
    estado = models.ForeignKey(
        Estado, on_delete=models.DO_NOTHING,
        related_name='feriado_estado',
        related_query_name='feriados_estados',
        null=True,
        db_column='cd_estado'
    )
    data = models.DateField()
    nome = models.CharField(
        max_length=100,
        db_column='nm_feriado'
    )

    class Meta:
        db_table = 'tb_feriado'

    def __str__(self):
        return f'{self.codigo}'
