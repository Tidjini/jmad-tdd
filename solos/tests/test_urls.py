from django.test import TestCase
from django.urls import resolve
from solos.views import index


class SolosUrlsTestCase(TestCase):

    def test_root_url_uses_index_view(self):
        '''
        Test that the root of the site resolve to the correct function
        '''
        root = resolve('/')
        self.assertEqual(root.func, index)

    def test_solo_details_url(self):
        '''
        Test that the url of the detail resolve to the correct function view
        '''
        solo_detail = resolve(
            '/recordings/kind-of-blue/all-blues/cannonbal-adderley/')
        self.assertEqual(solo_detail.func.__name__, 'solo_detail')

        self.assertEqual(solo_detail.kwargs['album'], 'kind-of-blue')
        self.assertEqual(solo_detail.kwargs['track'], 'all-blues')
        self.assertEqual(solo_detail.kwargs['artist'], 'cannonbal-adderley')
