from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.response import Response
from .serializers import *
from django.db.models import Count


class MarcaViewSet(GenericViewSet):

    def list(self, request):
        return Response(
            [{'label': x['marca'], 'value': x['marca']} for x in Referencia.objects.values('marca').annotate(
                annos=Count('anno')).order_by('marca')])


class AnnoViewSet(GenericViewSet):

    def list(self, request):
        return Response([{'label': x['anno'], 'value': x['anno']} for x in
                         Referencia.objects.filter(marca=request.GET.get('marca')).values('anno').annotate(
                             Count('valor')).order_by('marca', 'anno')])


class ModeloViewSet(GenericViewSet):

    def list(self, request):
        return Response([{'label': x['modelo'], 'value': x['modelo']} for x in
                         Referencia.objects.filter(marca=request.GET.get('marca'), anno=request.GET.get('anno')).values(
                             'modelo').annotate(
                             Count('valor')).order_by('marca', 'anno', 'modelo')])
