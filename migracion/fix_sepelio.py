import pandas as pd
from .models import *

def importar():
    xl = pd.ExcelFile('sepelio.xlsx')
    lista = xl.parse('Sheet1')

    for n in range(0, len(lista.ente)):
        try:
            empleado = Sepelio.objects.get(ente=lista.ente[n])
            print(empleado)
            empleado.desde = lista.desde[n]
            empleado.hasta = lista.hasta[n]
            empleado.nacimiento = lista.nacimiento[n]
            empleado.save()
        except:
            print("empleado no encontrado")


def chasis():
    xl = pd.ExcelFile('chasis.xlsx')
    lista = xl.parse('Sheet1')

    for n in range(0, len(lista.chasis)):
        try:
            auto = Auto.objects.get(chasis=lista.chasis[n])
            print(auto)
            auto.anno = lista.ano[n]
            auto.save()
        except:
            print("empleado no encontrado")