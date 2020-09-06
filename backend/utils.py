import calendar
from datetime import timedelta, datetime


def calcular_tabla_cuotas(prima_neta, comision, total, fecha_pago, cuotas, instance):
    def makerow(numero, today, fecha_pago, cuotas, monto_cuota):
        estado = 'VIGENTE' if today < fecha_pago else 'VENCIDO'
        mora = (today - fecha_pago).days
        return {'numero': numero, 'cuotas': cuotas, 'fecha': fecha_pago.strftime('%d/%m/%Y'),
                'monto': monto_cuota, 'saldo': monto_cuota,
                'monto_comision': monto_comision, 'estado': estado,
                'mora': mora}

    try:
        instance.cuotas().delete()
    except AttributeError:
        pass

    today = datetime.now()
    monto_cuota = round(total / cuotas, 2)
    monto_comision = round((prima_neta * (comision / 100)) / cuotas, 2)
    data = [makerow(1, today, fecha_pago, cuotas, monto_cuota), ]

    for i in range(1, cuotas):
        _, d = calendar.monthrange(fecha_pago.year, fecha_pago.month)
        fecha_pago = fecha_pago + timedelta(d)
        data.append(makerow(i + 1, today, fecha_pago, cuotas, monto_cuota))
    return data


def parse_date(strdate):
    try:
        return datetime.strptime(strdate, '%d/%m/%Y')
    except:
        return None
