from django.contrib import admin

from feriados.models import (
    Feriado
)


@admin.register(Feriado)
class Compra(admin.ModelAdmin):
    list_display = ('codigo', 'nome', 'data')
