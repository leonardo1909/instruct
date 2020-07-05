from django.conf.urls import include, url

from rest_framework import routers
from feriados.viewsets import (
    FeriadoViewSet, FeriadoMovelViewSet, FeriadoConsultaViewSet
)
from django.urls import re_path

router = routers.DefaultRouter()


urlpatterns = [
    url('', include(router.urls)),
    re_path(
        r'feriados/(?P<municipio__codigo_ibge>[0-9]{2}|[0-9]{7})/(?P<ano>[0-9]{4})-(?P<mes>[0-9]{2})-(?P<dia>[0-9]{2})/',
        FeriadoConsultaViewSet.as_view(),
        name='feriados'
    ),
    re_path(
        r'feriados/(?P<municipio__codigo_ibge>[0-9]{2}|[0-9]{7})/(?P<mes>[0-9]{2})-(?P<dia>[0-9]{2})/',
        FeriadoViewSet.as_view(),
        name='feriados'
    ),
    re_path(
        r'feriados/(?P<municipio__codigo_ibge>[0-9]{7})/(?P<feriado>[\w]+[-[\w]+[-[\w]+)/',
        FeriadoMovelViewSet.as_view(),
        name='feriados'
    )
]
