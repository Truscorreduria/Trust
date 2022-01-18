from backend.models import Oportunity, Campain, Ramo, SubRamo, Prospect, TipoDoc
from django.shortcuts import render
from .forms import AccidenteForm, VehiculoForm
from django.contrib.auth.models import User
import json


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


def cotiza_api(request):
    form = AccidenteForm()
    if request.method == "POST":
        form = AccidenteForm(request.POST)
        if form.is_valid():
            extra_data = {
                'profecion': form.cleaned_data.get('profecion'),
                'ocupacion': form.cleaned_data.get('ocupacion'),
                'suma_asegurada': form.cleaned_data.get('suma_asegurada'),
            }
            campain = Campain.objects.get(pk=90)
            ramo = Ramo.objects.get(pk=3)
            sub_ramo = SubRamo.objects.get(pk=21)
            user = User.objects.get(pk=2647)
            oportunidad = Oportunity()
            oportunidad.campain = campain
            oportunidad.ramo = ramo
            oportunidad.sub_ramo = sub_ramo
            oportunidad.vendedor = user
            oportunidad.prospect = get_prospect(form.cleaned_data)
            oportunidad.extra_data = json.dumps(extra_data, ensure_ascii=False)
            oportunidad.save()
            print(oportunidad.id)
        else:
            print(form.errors)
    return render(request, template_name="home/cotiza-api.html", context={
        'form': form
    })
