from django.test import TestCase, RequestFactory

from solos.views import index


class IndexViewTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_index_view_basic(self):
        '''
        Test that index view return 200 code with factory
        and uses the correct template
        '''
        request = self.factory.get('/')
        response = index(request)
        self.assertEqual(response.status_code, 200)