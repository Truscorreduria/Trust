from rest_framework import serializers
from backend.models import Referencia


class ReferenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Referencia
        fields = '__all__'

