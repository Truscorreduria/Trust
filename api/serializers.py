from rest_framework import serializers
from cotizador.models import Referencia


class ReferenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Referencia
        fields = '__all__'

