from datetime import datetime, timedelta
from pymeeus.Epoch import Epoch

from rest_framework import serializers
from feriados.models import Feriado, Municipio, Estado


class FeriadoSerializer(serializers.Serializer):
    name = serializers.CharField(
        max_length=100
    )

    def to_representation(self, instance):
        return {
            'name': instance.nome
        }

    def update(self, instance, validated_data):
        instance.nome = validated_data['name']
        instance.save()
        return instance

    def create(self, validated_data):
        estado = None
        municipio = None
        try:
            municipio = Municipio.objects.get(
                codigo_ibge=self.context['view'].kwargs['municipio__codigo_ibge']
            )
        except Municipio.DoesNotExist:
            try:
                estado = Estado.objects.get(
                    codigo_ibge=self.context['view'].kwargs['municipio__codigo_ibge']
                )
            except Estado.DoesNotExist:
                raise serializers.ValidationError(
                    {
                        'erro': 'O código informado é inválido.'
                    }
                )

        try:
            data = datetime(
                year=datetime.now().year,
                month=int(self.context['view'].kwargs['mes']),
                day=int(self.context['view'].kwargs['dia'])
            )
        except ValueError:
            raise serializers.ValidationError(
                {
                    'erro': 'a data informada não é válida.'
                }
            )

        feriado = Feriado(
            nome=validated_data['name'],
            municipio=municipio,
            estado=estado,
            data=data
        )
        feriado.save()

        return feriado


class FeriadoMovelSerializer(serializers.Serializer):

    def to_representation(self, instance):
        return {
            'name': instance.nome
        }

    def update(self, instance, validated_data):
        # instance.nome = validated_data['name']
        # instance.save()
        return instance

    def create(self, validated_data):
        estado = None
        municipio = None
        try:
            municipio = Municipio.objects.get(
                codigo_ibge=self.context['view'].kwargs['municipio__codigo_ibge']
            )
        except Municipio.DoesNotExist:
            try:
                estado = Estado.objects.get(
                    codigo_ibge=self.context['view'].kwargs['municipio__codigo_ibge']
                )
            except Estado.DoesNotExist:
                raise serializers.ValidationError(
                    {
                        'erro': 'O código informado é inválido.'
                    }
                )

        if str(self.context['view'].kwargs['feriado']).lower() == 'pascoa':
            ano = datetime.now().year
            pascoa_mes, pascoa_dia = Epoch.easter(ano)
            data = datetime(ano, pascoa_mes, pascoa_dia)
        elif str(self.context['view'].kwargs['feriado']).lower() == 'corpus-christi':
            ano = datetime.now().year
            pascoa_mes, pascoa_dia = Epoch.easter(ano)
            pascoa = datetime(ano, pascoa_mes, pascoa_dia)
            data = pascoa + timedelta(days=60)
        elif str(self.context['view'].kwargs['feriado']).lower() == 'sexta-feira-santa':
            ano = datetime.now().year
            pascoa_mes, pascoa_dia = Epoch.easter(ano)
            pascoa = datetime(ano, pascoa_mes, pascoa_dia)
            data = pascoa - timedelta(days=2)
        elif str(self.context['view'].kwargs['feriado']).lower() == 'carnaval':
            ano = datetime.now().year
            pascoa_mes, pascoa_dia = Epoch.easter(ano)
            pascoa = datetime(ano, pascoa_mes, pascoa_dia)
            data = pascoa - timedelta(days=47)
        else:
            raise serializers.ValidationError(
                {
                    'erro': 'O feriado inválido.'
                }
            )

        feriado = Feriado(
            nome=self.context['view'].kwargs['feriado'],
            municipio=municipio,
            estado=estado,
            data=data
        )
        feriado.save()

        return feriado
