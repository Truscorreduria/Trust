import pandas as pd
from .models import *

def get_departamento(name):
    d, created = Departamento.objects.get_or_create(name=name)
    return d

def importar():
    xl = pd.ExcelFile('departamentos.xlsx')
    lista = xl.parse('Hoja1')

    for n in range(0, len(lista.Ciudad)):
        d = get_departamento(lista.Ciudad[n])
        Municipio(name=lista.Municipio[n], departamento=d).save()