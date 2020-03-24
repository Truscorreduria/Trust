from django.urls import reverse, resolve
from django.test import TestCase


class TestMovieURLs(TestCase):
    #fixtures = ['movie.json', ]

    def test_urls(self):
        self.assertEqual(reverse('cotizador:inicio'), '/cotizador/')
        self.assertEqual(reverse('cotizador:get_data'), '/cotizador/get_data/')
        self.assertEqual(reverse('cotizador:guardar_poliza'), '/cotizador/guardar_poliza/')
        # self.assertEqual(reverse('movies:detail', kwargs={'id': '1'}), '/movies/1/')
        # self.assertEqual(reverse('movies:create'), '/movies/create/')
        # self.assertEqual(reverse('movies:update', kwargs={'id': '1'}), '/movies/update/1/')
        # self.assertEqual(resolve('/movies/update/1/').view_name, 'movies:update')
