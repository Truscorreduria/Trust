import calendar
from datetime import timedelta, datetime


def calcular_tabla_cuotas(prima_neta, comision, total, fecha_pago, cuotas, instance):
    try:
        instance.pagos().delete()
    except AttributeError:
        pass
    today = datetime.now()
    monto_cuota = round(total / cuotas, 2)
    monto_comision = round((prima_neta * (comision / 100)) / cuotas, 2)
    estado = 'VIGENTE' if today < fecha_pago else 'VENCIDO'
    data = [{'numero': 1, 'cuotas': cuotas, 'fecha': fecha_pago.strftime('%d/%m/%Y'), 'monto': monto_cuota,
             'monto_comision': monto_comision, 'estado': estado}]

    for i in range(1, cuotas):
        _, d = calendar.monthrange(fecha_pago.year, fecha_pago.month)
        fecha_pago = fecha_pago + timedelta(d)
        estado = 'VIGENTE' if today < fecha_pago else 'VENCIDO'
        data.append({'numero': i + 1, 'cuotas': cuotas, 'fecha': fecha_pago.strftime('%d/%m/%Y'), 'monto': monto_cuota,
                     'monto_comision': monto_comision, 'estado': estado})
    return data
