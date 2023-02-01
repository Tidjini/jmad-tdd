from django.test import TestCase, RequestFactory
from django.db.models.query import QuerySet
from solos.views import index
from solos.models import Solo


class IndexViewTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.drum_solo = Solo.objects.create(
            track='Bugle Call Rag',
            artist='Rich',
            instrument='drums'
        )
        self.bass_solo = Solo.objects.create(
            track='Mr. PC',
            artist='Coltrane',
            instrument='saxophone'
        )

    def test_index_view_basic(self):
        '''
        Test that index view return 200 code with factory
        and uses the correct template
        '''
        request = self.factory.get('/')

        with self.assertTemplateUsed('solos/index.html'):
            response = index(request)
            self.assertEqual(response.status_code, 200)

    def test_index_view_return_solos(self):
        """
        Test if index will attempt te return Solos if Query paramatters exist
        """
        response = self.client.get('/', {'instrument': 'drums'})
        solos = response.context['solos']
        self.assertIs(type(solos), QuerySet)
        self.assertEqual(len(solos), 1)
        self.assertEqual(solos[0].artist, 'Rich')
