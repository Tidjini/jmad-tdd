from django.test import TestCase

from solos.models import Solo
from albums.models import Album, Track
from unittest.mock import patch


class SoloModelTestCase(TestCase):

    def setUp(self):

        self.album = Album.objects.create(
            name='At the Startford Shakespearean Festival',
            artist="Oscar Peterson Trio",
            slug='at-the-startford-shakespearean-festival'
        )

        self.track = Track.objects.create(
            name='Falling in Love with Love',
            album=self.album,
            track_number=1,
            slug='falling-in-love-with-love'
        )
        self.solo = Solo.objects.create(
            track=self.track,
            artist='Oscar Peterson',
            instrument='piano',
            start_time='1:24',
            end_time='4:06',
            slug='oscar-peterson'
        )

    def test_solo_basic(self):
        '''
        Test the basic functionality of solo
        '''
        self.assertEqual(self.solo.artist, 'Oscar Peterson')
        self.assertEqual(self.solo.end_time, '4:06')

    def test_get_absolute_url(self):

        self.assertEqual(
            self.solo.get_absolute_url(),
            '/recordings/at-the-startford-shakespearean-festival/falling-in-love-with-love/oscar-peterson/'
        )

    @patch('musicbrainzngs.search_artists')
    def test_get_artist_tracks_from_musicbrainz(self, mock_mb_search_artists):
        # test that we can make Solos from the Musicbrainz API
        mock_mb_search_artists.return_value = {
            'artist-list': [
                {
                    'name': 'Jaco Pastorius',
                    'ext:score': '100',
                    'id': '48fze97-f7za89f7zae564EFA',
                    'tag-list': [
                        {
                            'count': '1',
                            'name': 'jazz fusion'
                        },
                        {
                            'count': '1',
                            'name': 'bassist'
                        }
                    ]
                }
            ]
        }

        created_solos = Solo.get_artist_tracks_from_musicbrainz(
            'Jaco Pastorius')
        mock_mb_search_artists.assert_called_with('Jaco Pastorius')

        self.assertEqual(len(created_solos), 2)
        self.assertEqual(created_solos[0].artist, 'Jaco Pastorius')
        self.assertEqual(created_solos[1].track.name, 'Donna Lee')
