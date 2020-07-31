from .models import *


def calcular_tabla_pagos(total, fecha_pago, cuotas, instance):
    try:
        instance.pagos().delete()
    except:
        pass
    monto_cuota = round(total / cuotas, 2)
    data = []
    anno = fecha_pago.year
    mes = fecha_pago.month
    dia = fecha_pago.day
    data.append({'numero': 1, 'cuotas': cuotas, 'fecha': fecha_pago.strftime('%d/%m/%Y'), 'monto': monto_cuota,
                 'monto_comision': 0.0, 'estado': 'VIGENTE'})
    for i in range(1, cuotas):
        if mes != 12:
            mes += 1
        else:
            mes = 1
            anno += 1
        fecha = valid_date(year=anno, month=mes, day=dia)
        data.append({'numero': i + 1, 'cuotas': cuotas, 'fecha': fecha.strftime('%d/%m/%Y'), 'monto': monto_cuota,
                     'monto_comision': 0.0, 'estado': 'VIGENTE'})
    return data
