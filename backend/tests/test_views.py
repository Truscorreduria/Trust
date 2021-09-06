from django.test import TestCase, RequestFactory
from frontend.apps.cotizador.views import *
from django.urls import reverse, resolve
import json


class Browser:
    family = 'Chrome'
    version_string = '1.0.0'


class Os:
    family = 'Linux'
    version_string = '1.0.0'


class Device:
    family = 'Linux'
    version_string = '1.0.0'


class UserAgent:
    is_mobile = False
    is_tablet = False
    is_pc = True
    is_bot = False
    browser = Browser()
    os = Os()
    device = Device()


# class TestHome(TestCase):
#     fixtures = ['referencia', 'aseguradora', 'user']
#     user = User.objects.get(username='abel')
#     user_agent = UserAgent()
#
#     def setUp(self):
#         self.request = RequestFactory()
#
#     def test_getdata(self):
#         request = self.request.post(reverse('cotizador:get_data'), {
#             'marca': 'MITSUBISHI',
#             'modelo': 'ASX',
#             'anno': '2017',
#             'chasis': '',
#             'exceso': '0.0',
#         })
#         request.user = self.user
#
#         response = get_data(request)
#         data = json.loads(response.content)
#         print(data)
#         self.assertEqual(response.status_code, 200)
#
#         request = self.request.post(reverse('cotizador:guardar_poliza'), {
#             'fecha_emision': '2019-11-19',
#             'nombres': get_profile(self.user).nombres,
#             'apellidos': get_profile(self.user).apellidos,
#             'email': self.user.email,
#             'cedula': get_profile(self.user).cedula,
#             'telefono': get_profile(self.user).telefono,
#             'celular': get_profile(self.user).celular,
#             'domicilio': get_profile(self.user).domicilio,
#             'anno': data['valor_nuevo']['anno'],
#             'marca': data['valor_nuevo']['marca'],
#             'modelo': data['valor_nuevo']['modelo'],
#             'chasis': data['valor_nuevo']['chasis'],
#             'motor': data['valor_nuevo']['motor'],
#             'valor_nuevo': data['valor_nuevo']['valor'],
#             'prima_total': data['prima_total'],
#             'emision': data['emision'],
#             'iva': data['iva'],
#             'total_pagar': data['prima_total'],
#             'cuotas': 12,
#             'circulacion': '252525',
#             'placa': '262626',
#             'color': 'AZUL',
#             'uso': 'PARTICULAR',
#             'porcentaje_deducible': data['porcentaje_deducible'],
#             'minimo_deducible': '0',
#             'porcentaje_deducible_extension': data['porcentaje_deducible_extension'],
#             'minimo_deducible_extension': data['minimo_deducible_extension'],
#             'deducible_rotura_vidrios': data['deducible_rotura_vidrios'],
#             'valor_depreciado': data['suma_asegurada'],
#             'monto_exceso': '0',
#             'costo_exceso': '0',
#             'tipo_cobertura': 'basica',
#             'medio_pago': 'deduccion_nomina',
#             'forma_pago': 'mensual',
#             'cesion_derecho': 'no',
#             'entidad': '',
#         })
#         request.user = self.user
#         request.user_agent = self.user_agent
#         response = guardar_poliza(request)
#         print(response.content)
#         self.assertEqual(response.status_code, 200)

    # def test_detail(self):
    #     resp = self.client.get('/movies/8/')
    #     self.assertEqual(resp.status_code, 200)
    #
    # def test_create(self):
    #     resp = self.client.get('/movies/create/')
    #     self.assertEqual(resp.status_code, 200)
    #
    #     resp = self.client.post('/movies/create/', {
    #         'title':'Testing in Production - The Movie',
    #         'year':'2019',
    #         'rated':'PG-13',
    #         'released_on':'2019-03-08',
    #         'genre':'Horror, Triller',
    #         'director':'William Palacios',
    #         'plot':'Even in 2019, after some years of software development evolution, some developers have adopted the horrible practice of testing in production...',
    #         'created_at':'2019-08-20T00:00:00+03:00',
    #         'updated_at':'2019-08-20T00:00:00+03:00'
    #     }, follow=True)
    #     self.assertEqual(resp.status_code, 200)
    #     self.assertContains(resp, 'Testing in Production - The Movie')
    #     self.assertContains(resp, 'The movie created successfully')
    #
    # def test_create_field_required(self):
    #     resp = self.client.post('/movies/create/', {
    #         'title':'',
    #         'year':'2019',
    #         'rated':'PG-13',
    #         'released_on':'2019-03-08',
    #         'genre':'Horror, Triller',
    #         'director':'William Palacios',
    #         'plot':'Even in 2019, after some years of software development evolution, some developers have adopted the horrible practice of testing in production...',
    #         'created_at':'2019-08-20T00:00:00+03:00',
    #         'updated_at':'2019-08-20T00:00:00+03:00'
    #     }, follow=True)
    #     self.assertContains(resp, 'The creation has failed')
    #     self.assertFormError(resp, 'form', 'title',
    #                          'This field is required.')
    #
    # def test_create_err_title_exists(self):
    #     resp = self.client.post('/movies/create/', {
    #         'title':'Testing in Production - The Movie',
    #         'year':'2019',
    #         'rated':'PG-13',
    #         'released_on':'2019-03-08',
    #         'genre':'Horror, Triller',
    #         'director':'William Palacios',
    #         'plot':'Even in 2019, after some years of software development evolution, some developers have adopted the horrible practice of testing in production...',
    #         'created_at':'2019-08-20T00:00:00+03:00',
    #         'updated_at':'2019-08-20T00:00:00+03:00'
    #     }, follow=True)
    #     print(resp)
    #     self.assertContains(resp, 'The creation has failed')
    #     self.assertFormError(resp, 'form', 'Title',
    #                          'Movie with this Title already exists.')
    #
    # def test_update(self):
    #     resp = self.client.get('/movies/update/8/')
    #     self.assertEqual(resp.status_code, 200)
    #
    #     resp = self.client.post('/movies/update/8/', {
    #         'title':'Tight Deadline without Well Defined Requirements',
    #         'year':'2019',
    #         'rated':'PG-13',
    #         'released_on':'2019-03-08',
    #         'genre':'Horror, Triller',
    #         'director':'Jose Matus',
    #         'plot':'Even in 2019, after some years of software development evolution, some developers have adopted the horrible practice of testing in production...',
    #         'created_at':'2019-08-20T00:00:00+03:00',
    #         'updated_at':'2019-08-20T00:00:00+03:00'
    #     }, follow=True)
    #     self.assertEqual(resp.status_code, 200)
    #     self.assertContains(resp, 'Jose Matus')
    #     self.assertContains(resp, 'The movie updated successfully')
    #
    # def test_update_wrong_release_date(self):
    #     resp = self.client.post('/movies/update/8/', {
    #         'title':'Tight Deadline without Well Defined Requirements',
    #         'year':'2019',
    #         'rated':'PG-13',
    #         'released_on':'a_release_date',
    #         'genre':'Horror, Triller',
    #         'director':'Jose Matus',
    #         'plot':'Even in 2019, after some years of software development evolution, some developers have adopted the horrible practice of testing in production...',
    #         'created_at':'2019-08-20T00:00:00+03:00',
    #         'updated_at':'2019-08-20T00:00:00+03:00'
    #     }, follow=True)
    #     self.assertContains(resp, 'The update has failed')
    #     self.assertFormError(resp, 'form', 'released_on', 'Enter a valid date.')
    #
    # def test_delete(self):
    #     resp = self.client.get('/movies/delete/8/')
    #     self.assertEqual(resp.status_code, 200)
    #
    #     resp = self.client.post('/movies/delete/8/', follow=True)
    #     self.assertContains(resp, 'The movie deleted successfully')
