from rest_framework.test import APITestCase

from albums.models import Album, Track
from solos.models import Solo


class SoloAPITestCase(APITestCase):

    def setUp(self):
        self.giant_steps = Album.objects.create(
            name='Giant Steps', slug='giant-steps')
        self.mr_pc = Track.objects.create(
            name='Mr. PC', slug='mr-pc', album=self.giant_steps)

    def test_create_solo(self):
        response = self.client.post('/api/solos/', {
            'track': '/api/tracks/2/',
            'artist': 'John Coltrane',
            'instrument': 'saxophone',
            'start_time': '0:24',
            'end_time': '3:21'
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, {
            'url': 'http://testserver/api/solos/1/',
            'track': 'http://testserver/api/tracks/2/',
            'artist': 'John Coltrane',
            'instrument': 'saxophone',
            'start_time': '0:24',
            'end_time': '3:21'
        })
