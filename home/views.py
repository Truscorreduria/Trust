from django.shortcuts import render
from .forms import *


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


def cotiza_auto(request):
    form = OportunityForm()
    return render(request, template_name="home/cotiza-auto.html", context={
        'form': form
    })
