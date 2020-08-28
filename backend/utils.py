import calendar
from datetime import timedelta


def calcular_tabla_cuotas(prima_neta, comision, total, fecha_pago, cuotas, instance):
    try:
        instance.pagos().delete()
    except AttributeError:
        pass
    monto_cuota = round(total / cuotas, 2)
    monto_comision = round((prima_neta * (comision / 100)) / cuotas, 2)
    data = [{'numero': 1, 'cuotas': cuotas, 'fecha': fecha_pago.strftime('%d/%m/%Y'), 'monto': monto_cuota,
             'monto_comision': monto_comision, 'estado': 'VIGENTE'}]

    for i in range(1, cuotas):
        _, d = calendar.monthrange(fecha_pago.year, fecha_pago.month)
        fecha_pago = fecha_pago + timedelta(d)
        data.append({'numero': i + 1, 'cuotas': cuotas, 'fecha': fecha_pago.strftime('%d/%m/%Y'), 'monto': monto_cuota,
                     'monto_comision': monto_comision, 'estado': 'VIGENTE'})
    return data
