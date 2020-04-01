from django.db.models import Sum
from easy_pdf.rendering import render_to_pdf_response, render_to_pdf
from .models import *
from django.http import JsonResponse
from grappelli_extras.utils import Codec
from django.views.decorators.csrf import csrf_exempt


def grabar_cobertura(request):
    obj = dict()
    if request.method == "POST":
        if 'cobertura' in request.POST:
            c = Cobertura.objects.get(id=request.POST.get('cobertura'))
        else:
            c = Cobertura()
            c.producto = Producto.objects.get(id=request.POST.get('producto'))
        c.name = request.POST.get('name')
        c.description = request.POST.get('description')
        c.tipo_calculo = request.POST.get('tipo_calculo')
        c.tipo_exceso = request.POST.get('tipo_exceso')
        c.tipo_cobertura = request.POST.get('tipo_cobertura')
        c.iva = request.POST.get('iva')
        c.save()
        for i in range(0, Aseguradora.objects.all().count()):
            a = request.POST.get('precios[%s][aseguradora]' % i)
            aseguradora = Aseguradora.objects.get(id=int(a))
            valor = request.POST.get('precios[%s][valor]' % i)
            available = request.POST.get('precios[%s][available]' % i)
            p, created = Precio.objects.get_or_create(aseguradora=aseguradora, cobertura=c)
            p.valor = float(valor)
            p.available = available
            p.save()
        obj = c.to_json()
    return JsonResponse(obj, encoder=Codec)


def eliminar_cobertura(request):
    obj = dict()
    if request.method == "POST":
        if 'cobertura' in request.POST:
            c = Cobertura.objects.get(id=request.POST.get('cobertura'))
            obj = c.to_json()
            c.delete()
    return JsonResponse(obj, encoder=Codec)


@csrf_exempt
def get_modelos(request):
    marca = request.POST.get('marca')
    modelos = Referencia.objects.filter(marca=marca).values(
        'modelo').annotate(models.Count('valor')).order_by('modelo')
    data = [x['modelo'] for x in modelos]
    return JsonResponse(data, safe=False)


@csrf_exempt
def get_valor(request):
    id = request.POST.get('original')
    marca = request.POST.get('marca')
    modelo = request.POST.get('modelo')
    anno = int(request.POST.get('anno'))

    referencias = Referencia.objects.filter(marca=marca, modelo=modelo).order_by('anno', 'chasis')
    if referencias.count() > 0:
        data = referencias.filter(anno=anno).order_by('anno', 'chasis')
        if data.count() > 0:
            referencias = data
        ref = referencias[0]
        valor_nuevo = ref.to_json()
    else:
        valor_nuevo = {'marca': marca, 'modelo': modelo, 'valor': 0.0}

    cotizacion = Cotizacion.objects.get(id=id)
    cotizacion.valor_nuevo = valor_nuevo['valor']
    cotizacion.anno = int(anno)
    cotizacion.save()
    cotizacion.crear_depreciacion()
    suma_asegurada = cotizacion.suma_asegurada()
    return JsonResponse({'valor_nuevo': valor_nuevo, 'suma_asegurada': suma_asegurada,
                         'referencias': [x.to_json() for x in referencias]}, safe=False, encoder=Codec)


@csrf_exempt
def suma_asegurada(request):
    id = request.POST.get('original')
    anno = request.POST.get('anno')
    valor_nuevo = request.POST.get('valor_nuevo')
    cotizacion = Cotizacion.objects.get(id=id)
    cotizacion.valor_nuevo = float(valor_nuevo)
    cotizacion.anno = int(anno)
    cotizacion.save()
    cotizacion.crear_depreciacion()
    suma_asegurada = cotizacion.suma_asegurada()
    return JsonResponse({'valor_nuevo': valor_nuevo, 'suma_asegurada': suma_asegurada}, safe=False, encoder=Codec)


@csrf_exempt
def generar_cotizacion(request):
    user = request.user
    c = Cotizacion.objects.get(id=request.POST.get('cotizacion', request.GET.get('contizacion')))
    costos = c.costos.all()
    aplica_iva = c.costos.filter(iva=True)
    suma_asegurada = ValorDepreciado.objects.filter(cotizacion=c)
    totales = []
    for a in c.aseguradora.all():
        subtotal = \
        Oferta.objects.filter(costo__in=costos, aseguradora=a, available=True).aggregate(Sum('quota_seguro'))[
            'quota_seguro__sum']
        monto_iva = \
        Oferta.objects.filter(costo__in=aplica_iva, aseguradora=a, available=True).aggregate(Sum('quota_seguro'))[
            'quota_seguro__sum']
        if monto_iva:
            emision = round(monto_iva * a.emision / 100, 2)
            iva = round((monto_iva + emision) * 0.15, 2)
        else:
            emision = 0.0
            iva = 0.0
        total = round((subtotal + emision + iva), 2)
        totales.append({'aseguradora': a, 'total': total, 'emision': emision, 'iva': iva})
    context = {'cotizacion': c, 'aseguradoras': c.aseguradora.all(), 'user': user,
               'suma_asegurada': suma_asegurada, 'totales': totales}
    # body = render_to_string('pdf/cotizacion.html', context)
    # cotizacion = render_to_pdf('pdf/cotizacion.html', context=context)
    # files = [("attachment", ("cotizacion.pdf", cotizacion)), ]
    # send_email("Has recibido un cupón", user.email, body, files=files)
    return render_to_pdf_response(request, 'pdf/cotizacion.html', context)
    # return render(request, 'pdf/cotizacion.html', context)



@csrf_exempt
def guardar_cotizacion(request):
    data = {
        'marca': request.POST.get('marca'),
        'modelo': request.POST.get('modelo'),
        'anno': request.POST.get('anno'),
        'nombres': request.POST.get('nombres'),
        'apellidos': request.POST.get('apellidos'),
        'cedula': request.POST.get('cedula'),
        'email': request.POST.get('email'),
        'valor_nuevo': request.POST.get('valor_nuevo'),
        'aseguradora': request.POST.get('aseguradora'),
        'valor_prima': request.POST.get('valor_prima'),
        'chasis': request.POST.get('chasis'),
        'motor': request.POST.get('motor'),
            }
    cotizacion = Cotizacion()
    cotizacion.producto = Producto.objects.get(code='0001')
    cotizacion.aseguradora = Aseguradora.objects.get(id=data['aseguradora'])
    cotizacion.nombres = data['nombres']
    cotizacion.apellidos = data['apellidos']
    cotizacion.cedula = data['cedula']
    cotizacion.email = data['email']
    cotizacion.tipo_auto = TIPO_AUTO[0][0]
    cotizacion.save()
    return JsonResponse(cotizacion.to_json(), encoder=Codec)