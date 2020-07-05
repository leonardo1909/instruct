from django.http import Http404
from django.db.models import Q

from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView, UpdateAPIView, DestroyAPIView,
    RetrieveAPIView
)

from feriados.utils.datas_moveis import verifica_feriado_movel
from feriados.models import Feriado
from feriados.serializers import (
    FeriadoSerializer, FeriadoMovelSerializer
)


class FeriadoConsultaViewSet(RetrieveAPIView):
    serializer_class = FeriadoSerializer
    lookup_field = 'municipio__codigo_ibge'
    lookup_url_kwarg = 'data'

    def get_queryset(self):
        if len(self.kwargs[self.lookup_field]) == 2:
            '''
                Retorna todos os feriados estaduais e nacionais.
            '''
            return Feriado.objects.filter(
                Q(estado__codigo_ibge=self.kwargs[self.lookup_field]) |
                (Q(estado__isnull=True) & Q(municipio__isnull=True)),
            )
        elif len(self.kwargs[self.lookup_field]) == 7:
            '''
                Retorna todos os feriado municipais, estaduais e nacionais.
            '''
            return Feriado.objects.filter(
                Q(municipio__codigo_ibge=self.kwargs[self.lookup_field]) |
                Q(estado__codigo_ibge=self.kwargs[self.lookup_field][:2]) |
                (Q(estado__isnull=True) & Q(municipio__isnull=True)),
            )

    def get_object(self):
        '''
            Busca no queryset o objeto a ser manipulado.
        '''
        queryset = self.filter_queryset(self.get_queryset())

        try:
            obj = queryset.get(
                data__day=self.kwargs['dia'],
                data__month=self.kwargs['mes']
            )
        except Feriado.DoesNotExist:
            raise Http404()

        return obj

    def retrieve(self, request, *args, **kwargs):
        sexta_santa = verifica_feriado_movel(
            self,
            ano=self.kwargs['ano'],
            mes=self.kwargs['mes'],
            dia=self.kwargs['dia'],
        )
        if sexta_santa:
            return Response(data=sexta_santa, status=status.HTTP_200_OK)

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class FeriadoViewSet(CreateAPIView, UpdateAPIView, DestroyAPIView):
    serializer_class = FeriadoSerializer
    lookup_field = 'municipio__codigo_ibge'
    lookup_url_kwarg = 'data'

    def get_queryset(self):
            return Feriado.objects.all()

    def get_object(self):
        '''
            Busca no queryset o objeto a ser manipulado.
        '''
        queryset = self.filter_queryset(self.get_queryset())

        try:
            obj = queryset.get(
                Q(municipio__codigo_ibge=self.kwargs[self.lookup_field]) |
                Q(estado__codigo_ibge=self.kwargs[self.lookup_field][:2])|
                (Q(estado__isnull=True) & Q(municipio__isnull=True)),
                data__day=self.kwargs['dia'],
                data__month=self.kwargs['mes']
            )
        except Feriado.DoesNotExist:
            raise Http404()

        return obj

    def put(self, request, *args, **kwargs):
        try:
            return self.update(request, *args, **kwargs)
        except Http404:
            return self.create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if len(kwargs['municipio__codigo_ibge']) == 7 and instance.municipio is None:
            return Response(status=status.HTTP_403_FORBIDDEN)
        elif len(kwargs['municipio__codigo_ibge']) == 2 and instance.estado is None:
            return Response(status=status.HTTP_403_FORBIDDEN)

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class FeriadoMovelViewSet(CreateAPIView, UpdateAPIView, DestroyAPIView):
    serializer_class = FeriadoMovelSerializer
    lookup_field = 'municipio__codigo_ibge'
    lookup_url_kwarg = 'feriado'

    def get_queryset(self):
        return Feriado.objects.all()

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        try:
            obj = queryset.get(
                Q(municipio__codigo_ibge=self.kwargs[self.lookup_field]) |
                Q(estado__codigo_ibge=self.kwargs[self.lookup_field]),
                nome=self.kwargs[self.lookup_url_kwarg].replace('-', ' ').title()
            )
        except Feriado.DoesNotExist:
            raise Http404()

        return obj

    def put(self, request, *args, **kwargs):
        try:
            return self.update(request, *args, **kwargs)
        except Http404:
            return self.create(request, *args, **kwargs)
