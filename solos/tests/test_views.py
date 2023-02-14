from django.test import TestCase, RequestFactory
from django.db.models.query import QuerySet
from solos.views import index, solo_detail
from solos.models import Solo
from albums.models import Album, Track


class SoloBaseTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.no_funny_hats = Album.objects.create(
            name='No Funny Hats', slug='no-funny-hats'
        )
        cls.bugle_call_rag = Track.objects.create(
            name='Bugle Call Rag', slug='bugle-call-rag',
            album=cls.no_funny_hats
        )
        cls.drum_solo = Solo.objects.create(
            track=cls.bugle_call_rag,
            artist='Buddy Rich',
            instrument='drums',
            slug='buddy-rich'
        )

        cls.giants_steps = Album.objects.create(
            name='Giants Steps', slug='giants-steps'
        )
        cls.mr_pc = Track.objects.create(
            name='Mr. PC', slug='mr-pc', album=cls.giants_steps
        )

        cls.sax_solo = Solo.objects.create(
            track=cls.mr_pc,
            artist='Coltrane',
            instrument='saxophone',
            slug='coltrane'
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
        self.assertEqual(solos[0].artist, 'Buddy Rich')


class SoloViewTestCase(SoloBaseTestCase):

    def test_basic(self):
        '''check page response is 200, and usees the correct template, and has the correct context'''
        request = self.factory.get(
            '/recordings/no-funny-hats/bugle-call-rag/buddy-rich/'
        )

        with self.assertTemplateUsed('solos/solo_detail.html'):
            response = solo_detail(
                request,
                album=self.no_funny_hats.slug,
                track=self.bugle_call_rag.slug,
                artist=self.drum_solo.slug
            )

        self.assertEqual(response.status_code, 200)
        page = response.content.decode()
        self.assertInHTML('<p id="jmad-artist">Buddy Rich</p>', page)
        self.assertInHTML(
            '<p id="jmad-track">Bugle Call Rag [1 solo]</p>', page)
