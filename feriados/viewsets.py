from django.http import Http404
from django.db.models import Q

from rest_framework.generics import (
    CreateAPIView, UpdateAPIView, DestroyAPIView,
    ListAPIView
)

from feriados.models import Feriado
from feriados.serializers import (
    FeriadoSerializer, FeriadoMovelSerializer
)
# from rest_framework.response import Response
# from rest_framework import status


class FeriadoViewSet(ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView):
    serializer_class = FeriadoSerializer
    lookup_field = 'municipio__codigo_ibge'
    lookup_url_kwarg = 'data'

    def get_queryset(self):
        if len(self.kwargs[self.lookup_field]) == 2:
            return Feriado.objects.filter(
                data__day=self.kwargs['dia'],
                data__month=self.kwargs['mes'],
                estado__codigo_ibge=self.kwargs[self.lookup_field]
            )
        elif len(self.kwargs[self.lookup_field]) == 7:
            return Feriado.objects.filter(
                data__day=self.kwargs['dia'],
                data__month=self.kwargs['mes'],
                municipio__codigo_ibge=self.kwargs[self.lookup_field]
            )
        else:
            return Feriado.objects.all()

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        try:
            obj = queryset.get(
                Q(municipio__codigo_ibge=self.kwargs[self.lookup_field]) |
                Q(estado__codigo_ibge=self.kwargs[self.lookup_field]),
            )
        except Feriado.DoesNotExist:
            raise Http404()

        return obj

    # def get(self, request, codigo_ibge, data):
    #     return Response(
    #         status=status.HTTP_200_OK
    #     )

    def put(self, request, *args, **kwargs):
        try:
            return self.update(request, *args, **kwargs)
        except Http404:
            return self.create(request, *args, **kwargs)


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
                nome=self.kwargs[self.lookup_url_kwarg]
            )
        except Feriado.DoesNotExist:
            raise Http404()

        return obj

    def put(self, request, *args, **kwargs):
        try:
            return self.update(request, *args, **kwargs)
        except Http404:
            return self.create(request, *args, **kwargs)
