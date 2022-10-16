from .models import Comentario
from django.views.generic import View
from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType


class Comentarios(View):
    template_name = 'backend/bitacora/history.html'

    def get(self, request, *args, **kwargs):
        host = request.get_host()
        pre_url = request.META.get('HTTP_REFERER').split(host)[1]
        app_label, model_name, object_id = pre_url.split('/')[2:5]
        content_type = ContentType.objects.get(app_label=app_label, model=model_name)
        instance = content_type.model_class().objects.get(pk=object_id)
        queryset = Comentario.bitacora(instance)
        return render(request, self.template_name, {
            'queryset': queryset,
            'instance': instance,
            'options': instance._meta
        })
