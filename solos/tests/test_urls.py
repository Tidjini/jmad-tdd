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

    def test_solo_detail_url(self):
        '''
        Test that the url of the detail resolve to the correct function view
        '''
        solo_detail = resolve('/solos/1/')
        self.assertEqual(solo_detail.func.__name__, 'view')
        self.assertEqual(solo_detail.kwargs['pk'], '1')
