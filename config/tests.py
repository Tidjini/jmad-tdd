from django.test import LiveServerTestCase
from django.contrib.auth import get_user_model
from selenium import webdriver
from selenium.webdriver.common.by import By

from solos.models import Solo
from albums.models import Album, Track


class StudentTestCase(LiveServerTestCase):

    INSTRUMENT_INPUT_ID = 'jmad-instrument'
    ARTIST_INPUT_ID = 'jmad-artist'

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(5)

        self.admin_user = get_user_model().objects.create_superuser(
            username='bill',
            email='bill@example.com',
            password='password'
        )

        self.album1 = Album.objects.create(
            name='My Favorite Things', slug='my-favorite-things'
        )
        self.track1 = Track.objects.create(
            name='My Favorite Things', slug='my-favorite-things',
            album=self.album1
        )

        self.solo1 = Solo.objects.create(
            track=self.track1,
            artist='John Coltrane',
            instrument='saxophone',
            slug='john-coltrane'
        )

        self.album2 = Album.objects.create(
            name='Kind of Blue', slug='kind-of-blue',
        )
        self.track2 = Track.objects.create(
            name='All Blues', slug='all-blues',
            album=self.album2, track_number=4
        )

        self.solo2 = Solo.objects.create(
            track=self.track2,
            start_time='2:06',
            end_time='4:01',
            artist='Cannonball Adderley',
            instrument='saxophone',
            slug='cannonball-adderley'
        )

        self.album3 = Album.objects.create(
            name='Know What I Mean?', slug='know-what-i-mean'
        )
        self.track3 = Track.objects.create(
            name='Waltz for Debby', slug='waltz-for-debby',
            album=self.album3
        )

        self.track4 = Track.objects.create(
            name='Freeddie Freeloader', album=self.album2
        )
        self.track5 = Track.objects.create(
            name='Blue in Green', album=self.album2
        )
        self.solo3 = Solo.objects.create(
            track=self.track3,
            artist='Cannonball Adderley',
            instrument='saxophone',
            slug='cannonball-adderley'
        )

        self.solo4 = Solo.objects.create(
            track=self.track2,
            artist='Miles Davis',
            instrument='trumpet',
            slug='miles-davis'
        )

    def find_search_results(self):
        return self.browser.find_elements(By.CSS_SELECTOR, '.jmad-search-result a')

    def test_student_find_solos(self):
        """
        test that a user can search for solos
        """
        # Steve example write todo later
        home_page = self.browser.get(self.live_server_url + '/')
        brand_element = self.browser.find_element(
            By.CLASS_NAME, 'navbar-brand')
        self.assertEqual('JMAD', brand_element.text)

        # He sees the input search form, including labels and placeholder

        instrument_input = self.browser.find_element(
            By.CSS_SELECTOR, f'input#{self.INSTRUMENT_INPUT_ID}')
        self.assertIsNotNone(self.browser.find_element(
            By.CSS_SELECTOR, f'label[for="jmad-instrument"]'))
        self.assertEqual(instrument_input.get_attribute(
            'placeholder'), 'i.e. trumpet')

        artist_input = self.browser.find_element(
            By.CSS_SELECTOR, f'input#{self.ARTIST_INPUT_ID}')
        self.assertIsNotNone(self.browser.find_element(
            By.CSS_SELECTOR, f'label[for="jmad-artist"]'))
        self.assertEqual(artist_input.get_attribute(
            'placeholder'), 'i.e. davis')
        # handling the inputs typing

        # handling the inputs typing
        instrument_input.send_keys('saxophone')
        # instrument_input.submit()

        # he sees many results, so he adds a particular
        # artist to his search query
        searched_results = self.find_search_results()
        self.assertGreater(len(searched_results), 2)

        # ...so he adds a particular artist to his search query, and gets
        # more manageble list
        second_artist_input = self.browser.find_element(
            By.CSS_SELECTOR, f'input#{self.ARTIST_INPUT_ID}')
        second_artist_input.send_keys('Cannonball Adderley')
        # second_artist_input.submit()
        self.browser.find_element(By.CSS_SELECTOR, 'form button').click()

        second_searched_results = self.find_search_results()
        self.assertEqual(len(second_searched_results), 2)

        # He clicks on search results
        second_searched_results[0].click()

        # in the solo page he sees, title, artist and album of this particular solo
        import pdb
        pdb.set_trace()
        self.assertEqual(self.browser.current_url,
                         self.live_server_url +
                         '/recordings/kind-of-blue/all-blues/cannonball-adderley/'
                         )

        # he sees the artist
        self.assertEqual(
            self.browser.find_element(By.CSS_SELECTOR, '#jmad-artist').text,
            'Cannonball Adderley'
        )
        # the track title (with count of solos)
        self.assertEqual(
            self.browser.find_element(By.CSS_SELECTOR, "#jmad-track").text,
            'All Blues [2 solos]'
        )

        # and the album title (with track count) for this solo
        self.assertEqual(
            self.browser.find_element(By.CSS_SELECTOR, '#jmad-album').text,
            'Kind of Blue [3 tracks]'
        )

    def test_staff_can_add_content(self):
        # Test Staff Acces to admin page
        admin_root = self.browser.get(self.live_server_url + '/admin/')
        # staff can tell he is in right place by the title
        self.assertEqual(self.browser.title, 'Log in | Django site admin')

        # He enters his name and password to login
        login_form = self.browser.find_element(By.ID, 'login-form')

        login_form.find_element(By.NAME, 'username').send_keys('bill')
        login_form.find_element(By.NAME, 'password').send_keys('password')
        login_form.find_element(By.CSS_SELECTOR, '.submit-row input').click()

        import pdb
        pdb.set_trace()

        self.fail('Incomplete Test')
        # Test adding record and solos number

        # staff is in the right place because of the title
        #
        # username & password to login
        #
        # sees links to Albums, Tracks, Solos

    def tearDown(self):
        self.browser.quit()
