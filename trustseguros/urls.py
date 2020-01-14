from django.urls import path
from .views import *


app_name = "trustseguros"


urlpatterns = [

    #urls para el sitio administrativo

    path('documentos/', documentos, name="documentos"),
    path('certificados/', certificados, name="certificados"),
    path('certificado/', certificado, name="certificado"),
    path('importar_polizas/', ImportPoliza.as_view(), name="importar_polizas"),
    path('import_person/', ImportPerson.as_view(), name="import_person"),
    path('import_company/', ImportCompany.as_view(), name="import_company"),
    path('importar_certificado_edificio/', ImportCertificadoEdificio.as_view(), name="importar_certificado_edificio"),
    path('importar_certificado_auto/', ImportCertificadoAuto.as_view(), name="importar_certificado_auto"),
    path('importar_certificado_persona/', ImportCertificadoPersona.as_view(), name="importar_certificado_persona"),
    path('download/', download, name="download"),


    #url lte

    path('', index, name="index"),
    path('naturales/', ClientesNaturales.as_view(), name="clientes_naturales"),
    path('juridicos/', ClientesJuridicos.as_view(), name="clientes_juridicos"),
    path('aseguradoras/', Aseguradoras.as_view(), name="aseguradoras"),
    path('polizas/', Polizas.as_view(), name="polizas"),
    path('tramites/', Tramites.as_view(), name="tramites"),
    path('endosos/', Endosos.as_view(), name="endosos"),


    path('usuarios/', Usuarios.as_view(), name="usuarios"),
    path('sepelio/', DependientesSepelio.as_view(), name="sepelio"),
    path('accidente/', DependientesAccidente.as_view(), name="accidente"),
    path('automovil/', PolizasAutomovil.as_view(), name="automovil"),
    path('tickets/', Tickets.as_view(), name="tickets"),

]
