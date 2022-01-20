from backend.models import Oportunity, Campain, Ramo, SubRamo, Prospect, Linea, Grupo
from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string
from .forms import AccidenteForm, VehiculoForm
from django.contrib.auth.models import User
import json
from django.views.generic import View
from utils.utils import send_email, send_sms
from django.urls import reverse


def index(request):
    return render(request, template_name="home/index.html")


def lineas(request):
    return render(request, template_name="home/lineas.html")


def nosotros(request):
    return render(request, template_name="home/nosotros.html")


def corredor(request):
    return render(request, template_name="home/corredor.html")


def plataformas(request):
    return render(request, template_name="home/plataformas.html")


def politicas(request):
    return render(request, template_name="home/politicas.html")


def contacto(request):
    return render(request, template_name="home/contacto.html")


def get_prospect(cleaned_data):
    prospect, _ = Prospect.objects.get_or_create(tipo_identificacion=cleaned_data.get('tipo_doc'),
                                                 cedula=cleaned_data.get('identificacion'))
    prospect.primer_nombre = cleaned_data.get('primer_nombre')
    prospect.segundo_nombre = cleaned_data.get('segundo_nombre')
    prospect.apellido_paterno = cleaned_data.get('apellido_paterno')
    prospect.apellido_materno = cleaned_data.get('apellido_materno')
    prospect.celular = cleaned_data.get('celular')
    prospect.email_personal = cleaned_data.get('email_personal')
    prospect.save()
    return prospect


def cotiza_auto(request):
    form = VehiculoForm()
    if request.method == "POST":
        print(request.POST)
        form = VehiculoForm(request.POST)
        if form.is_valid():
            pass
    return render(request, template_name="home/cotiza-auto.html", context={
        'form': form
    })


class CotizaApi(View):
    form = AccidenteForm
    container_template = "home/form-container.html"
    form_content = "home/cotiza-api.html"

    def get(self, request):
        return render(request, template_name=self.container_template, context={
            'form': self.form(), 'form_content': self.form_content
        })

    def post(self, request):
        result = 'error'
        html_form = ''
        form = AccidenteForm(request.POST)
        if form.is_valid():
            extra_data = {
                'PROFESION': form.cleaned_data.get('profecion'),
                'OCUPACION': form.cleaned_data.get('ocupacion'),
                'SUMA_ASEGURADA': form.cleaned_data.get('suma_asegurada'),
            }
            linea = Linea.objects.get(pk=4)
            campain = Campain.objects.get(pk=90)
            ramo = Ramo.objects.get(pk=3)
            sub_ramo = SubRamo.objects.get(pk=21)
            user = User.objects.get(pk=2647)
            grupo = Grupo.objects.get(pk=4)
            oportunidad = Oportunity()
            oportunidad.grupo = grupo
            oportunidad.linea = linea
            oportunidad.campain = campain
            oportunidad.ramo = ramo
            oportunidad.sub_ramo = sub_ramo
            oportunidad.vendedor = user
            oportunidad.prospect = get_prospect(form.cleaned_data)
            oportunidad.extra_data = json.dumps(extra_data, ensure_ascii=False)
            oportunidad.save()
            result = 'success'
            url = request.build_absolute_uri(reverse("trustseguros:oportunidades", kwargs={"linea": linea.id}))
            send_email(f'Nueva contizacion de accidentes personales', grupo.email_notificacion,
                       f'{url}')
            send_sms(f'Estimado(a) {oportunidad.prospect.primer_nombre} {oportunidad.prospect.apellido_paterno}, '
                     f'Le saluda Trust Correduria. Su cotización está en proceso, '
                     f'para consultas llamar o escribir al 87425466',
                     oportunidad.prospect.celular)
        else:
            html_form = render_to_string(self.form_content, {
                'form': form,
            }, request)
        return JsonResponse({
            'result': result,
            'form': html_form
        })
