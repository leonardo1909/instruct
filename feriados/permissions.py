from datetime import datetime, timedelta
from pymeeus.Epoch import Epoch

from django.db.models import Q

from rest_framework.exceptions import ValidationError
from rest_framework import permissions

from feriados.models import Feriado


class FeriadoNacionalPermission(permissions.BasePermission):
    message = 'Não permitido'

    def has_permission(self, request, view):
        ano = datetime.now().year
        try:
            data = datetime(
                year=datetime.now().year,
                month=int(view.kwargs['mes']),
                day=int(view.kwargs['dia'])
            )
        except ValueError:
            return ValidationError(
                {
                    'erro': 'data inválida.'
                }
            )

        feriado_nacional_fixo = Feriado.objects.filter(
            (Q(estado__isnull=True) & Q(municipio__isnull=True)),
            data=data
        )

        pascoa_mes, pascoa_dia = Epoch.easter(ano)
        pascoa = datetime(ano, pascoa_mes, pascoa_dia)
        sexta_santa = pascoa - timedelta(days=2)
        if feriado_nacional_fixo or pascoa or sexta_santa:
            return False

        return True
