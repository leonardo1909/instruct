from datetime import datetime, timedelta
from pymeeus.Epoch import Epoch

from django.db.models import Q

from feriados.models import Feriado


def verifica_feriado_movel(self, ano, mes, dia):
    '''
        Verifica se a data passada é algum feriado móvel.
        Para feriados movéis que não são nacionais, verifica se o feriado
        já está cadastrado para o municipio.
    '''
    data_analisada = datetime(int(ano), int(mes), int(dia))
    pascoa_mes, pascoa_dia = Epoch.easter(int(ano))
    pascoa = datetime(int(ano), pascoa_mes, pascoa_dia)

    if data_analisada == pascoa - timedelta(days=2):
        return {
            'name': 'Sexta-Feira Santa'
        }
    elif data_analisada == pascoa:
        feriado_pascoa = Feriado.objects.filter(
            Q(municipio__codigo_ibge=self.kwargs['municipio__codigo_ibge']) |
            Q(estado__codigo_ibge=self.kwargs['municipio__codigo_ibge'][:2]),
            nome='Pascoa'
        )
        if not feriado_pascoa:
            return None
        else:
            return {
                'name': 'Pascoa'
            }
    elif data_analisada == pascoa - timedelta(days=47):
        feriado_carnaval = Feriado.objects.filter(
            Q(municipio__codigo_ibge=self.kwargs['municipio__codigo_ibge']) |
            Q(estado__codigo_ibge=self.kwargs['municipio__codigo_ibge'][:2]),
            nome='Carnaval'
        )
        if not feriado_carnaval:
            return None
        else:
            return {
                'name': 'Carnaval'
            }
    elif data_analisada == pascoa + timedelta(days=60):
        feriado_corpus_christi = Feriado.objects.filter(
            Q(municipio__codigo_ibge=self.kwargs['municipio__codigo_ibge']) |
            Q(estado__codigo_ibge=self.kwargs['municipio__codigo_ibge'][:2]),
            nome='Corpus Christi'
        )
        if not feriado_corpus_christi:
            return None
        else:
            return {
                'name': 'Corpus Christi'
            }
    else:
        return None
