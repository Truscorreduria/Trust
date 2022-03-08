import calendar
from datetime import timedelta, datetime
from openpyxl import Workbook
from django.http import HttpResponse


def render_to_excell(data, filename="Reporte.xlsx"):
    book = Workbook()
    sheet = book.active
    for row in data:
        sheet.append(row)
    response = HttpResponse(content_type="application/ms-excel")
    content = "attachment; filename={0}".format(filename)
    response["Content-Disposition"] = content
    book.save(response)
    return response


def daysOfNextMont(last_day):
    firstDay = last_day + timedelta(1)
    return calendar.monthrange(firstDay.year, firstDay.month)[1]


def calcular_tabla_cuotas(prima_neta, comision, total, fecha_pago, cuotas, instance):
    def makerow(numero, today, fecha_pago, cuotas, monto_cuota):
        estado = 'VIGENTE' if today < fecha_pago else 'VENCIDO'
        mora = (today - fecha_pago).days
        return {'numero': numero, 'cuotas': cuotas, 'fecha': fecha_pago.strftime('%d/%m/%Y'),
                'monto': monto_cuota, 'saldo': monto_cuota,
                'monto_comision': monto_comision, 'estado': estado,
                'mora': mora}

    try:
        if not instance.con_pagos():
            instance.cuotas().delete()
    except AttributeError:
        pass

    today = datetime.today()
    monto_cuota = round(total / cuotas, 2)
    monto_comision = round((prima_neta * (comision / 100)) / cuotas, 2)
    data = [makerow(1, today, fecha_pago, cuotas, monto_cuota), ]

    days = fecha_pago.day
    for i in range(1, cuotas):
        _, d = calendar.monthrange(fecha_pago.year, fecha_pago.month)
        last_day = datetime(fecha_pago.year, fecha_pago.month, d)
        donm = daysOfNextMont(last_day)
        if days > donm:
            fecha_pago = last_day + timedelta(donm)
        else:
            fecha_pago = last_day + timedelta(days)
        data.append(makerow(i + 1, today, fecha_pago, cuotas, monto_cuota))
    return data


def parse_date(strdate):
    try:
        return datetime.strptime(strdate, '%d/%m/%Y')
    except:
        return None
