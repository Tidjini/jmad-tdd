from django.test import TestCase

from solos.models import Solo


class SoloModelTestCase(TestCase):

    def setUp(self):
        self.solo = Solo.objects.create(
            track='Falling in Love with Love',
            artist='Peterson',
            instrument='Piano'
        )

    def test_solo_basic(self):
        '''
        Test the basic functionality of solo 
        '''
        self.assertEqual(self.solo.artist, 'Peterson')
