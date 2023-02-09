from django.test import TestCase, RequestFactory
from django.db.models.query import QuerySet
from solos.views import index, SoloDetailView
from solos.models import Solo


class SoloBaseTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.drum_solo = Solo.objects.create(
            track='Bugle Call Rag',
            artist='Rich',
            instrument='drums'
        )
        cls.bass_solo = Solo.objects.create(
            track='Mr. PC',
            artist='Coltrane',
            instrument='saxophone'
        )


class IndexViewTestCase(SoloBaseTestCase):

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


class SoloViewTestCase(SoloBaseTestCase):

    def test_basic(self):
        '''check page response is 200, and usees the correct template, and has the correct context'''
        request = self.factory.get('/solo/1/')
        response = SoloDetailView.as_view()(request, self.drum_solo.pk)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.contex_data['solo'].artis, 'Rich')
        with self.assertTemplateUsed('solos/solo_detail.html'):
            response.render()
