from django.test import LiveServerTestCase
from django.contrib.auth import get_user_model
from selenium import webdriver
from selenium.webdriver.common.by import By

from solos.models import Solo
from albums.models import Album, Track

# functional tests


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
            name='Freddie Freeloader', album=self.album2, track_number=2
        )
        self.track5 = Track.objects.create(
            name='Blue in Green', album=self.album2, track_number=3
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
            slug='miles-davis',
            start_time='1:46',
            end_time='4:04'
        )

    def find_search_results(self):
        return self.browser.find_elements(By.CSS_SELECTOR, '.jmad-search-result a')

    def test_student_find_solos(self):
        """
        test that a user can search for solos
        """
        # Steve can enter to home page
        home_page = self.browser.get(self.live_server_url + '/')

        # Steve can show See JMAD in navbar
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

        # He sees links to Album, Tracks, and Solos

        album_links = self.browser.find_element(By.LINK_TEXT, 'Albums')
        self.assertEqual(
            album_links.get_attribute('href'),
            self.live_server_url + '/admin/albums/album/'
        )

        self.assertEqual(
            self.browser.find_element(
                By.LINK_TEXT, 'Tracks').get_attribute('href'),
            self.live_server_url + '/admin/albums/track/'
        )

        solo_links = self.browser.find_element(By.LINK_TEXT, 'Solos')
        self.assertEqual(
            solo_links.get_attribute('href'),
            self.live_server_url + '/admin/solos/solo/'
        )

        # he click on album link to display all albums added
        album_links.click()

        self.assertEqual(
            self.browser.find_element(
                By.LINK_TEXT, 'Know What I Mean?').get_attribute('href'),
            self.live_server_url + '/admin/albums/album/3/change/'
        )

        self.assertEqual(
            self.browser.find_element(
                By.LINK_TEXT, 'Kind of Blue').get_attribute('href'),
            self.live_server_url + '/admin/albums/album/2/change/'
        )

        self.assertEqual(
            self.browser.find_element(
                By.LINK_TEXT, 'My Favorite Things').get_attribute('href'),
            self.live_server_url + '/admin/albums/album/1/change/'
        )

        # he going back to root and click on track link
        self.browser.find_element(By.CSS_SELECTOR, '#site-name a').click()

        self.browser.find_element(By.LINK_TEXT, 'Tracks').click()

        track_rows = self.browser.find_elements(
            By.CSS_SELECTOR, '#result_list tr')

        self.assertEqual(track_rows[1].text,
                         'Kind of Blue Freddie Freeloader 2')
        self.assertEqual(track_rows[2].text, 'Kind of Blue Blue in Green 3')
        self.assertEqual(track_rows[3].text, 'Kind of Blue All Blues 4')
        self.assertEqual(track_rows[4].text,
                         'Know What I Mean? Waltz for Debby -')
        self.assertEqual(
            track_rows[5].text, 'My Favorite Things My Favorite Things -')

        self.browser.find_element(By.LINK_TEXT, 'ADD TRACK').click()

        self.browser.find_element(By.NAME, 'name').send_keys('So What')
        self.browser.find_element(By.NAME, 'album').find_elements(
            By.TAG_NAME, 'option')[1].click()
        self.browser.find_element(By.NAME, 'track_number').send_keys('1')
        self.browser.find_element(By.NAME, 'slug').send_keys('so-what')
        self.browser.find_element(By.CSS_SELECTOR, '.submit-row input').click()
        self.assertEqual(self.browser.find_elements(By.CSS_SELECTOR, '#result_list tr')[
                         1].text, 'Kind of Blue So What 1')

        # he adds another track, this time on album that not exist
        self.browser.find_element(By.LINK_TEXT, 'ADD TRACK').click()
        track_form = self.browser.find_element(By.ID, 'track_form')
        track_form.find_element(By.NAME, 'name').send_keys(
            'My Funny Valentine')
        # he clicks oon add a new album
        track_form.find_element(By.ID, 'add_id_album').click()
        # on new window he adds album information
        self.browser.switch_to.window(self.browser.window_handles[1])
        album_form = self.browser.find_element(By.ID, 'album_form')
        album_form.find_element(By.NAME, 'name').send_keys("Cookin'")
        album_form.find_element(By.NAME, 'artist').send_keys(
            "Miles Davis Quintet")
        album_form.find_element(By.NAME, 'slug').send_keys("cookin")
        self.browser.find_element(By.CSS_SELECTOR, '.submit-row input').click()

        # after creating album he continue adding track information
        self.browser.switch_to.window(self.browser.window_handles[0])
        track_form = self.browser.find_element(By.ID, 'track_form')
        track_form.find_element(By.NAME, 'track_number').send_keys('1')
        track_form.find_element(By.NAME, 'slug').send_keys(
            'my-funny-valentine')
        track_form.find_element(By.CSS_SELECTOR, '.submit-row input').click()
        self.assertEqual(self.browser.find_elements(By.CSS_SELECTOR, '#result_list tr')[
                         1].text, "Cookin' My Funny Valentine 1")

        # he goes back to main and adds new solo
        self.browser.find_element(By.CSS_SELECTOR, '#site-name a').click()
        self.browser.find_element(By.LINK_TEXT, 'Solos').click()

        solo_rows = self.browser.find_elements(
            By.CSS_SELECTOR, '#result_list tr')
        self.assertEqual(solo_rows[1].text, 'All Blues Miles Davis 1:46-4:04')
        self.assertEqual(solo_rows[2].text,
                         'All Blues Cannonball Adderley 2:06-4:01')
        self.assertEqual(solo_rows[3].text,
                         'Waltz for Debby Cannonball Adderley')
        self.assertEqual(solo_rows[4].text, 'My Favorite Things John Coltrane')

        # He adds a solo to existed Track
        self.browser.find_element(By.LINK_TEXT, 'ADD SOLO').click()
        solo_form = self.browser.find_element(By.ID, 'solo_form')
        solo_form.find_element(By.NAME, 'track').find_elements(
            By.TAG_NAME, 'option')[7].click()
        solo_form.find_element(By.NAME, 'artist').send_keys('McCoy Tyner')
        solo_form.find_element(By.NAME, 'instrument').send_keys('Piano')
        solo_form.find_element(By.NAME, 'start_time').send_keys('2:19')
        solo_form.find_element(By.NAME, 'end_time').send_keys('7:01')
        solo_form.find_element(By.NAME, 'slug').send_keys('mcoy-tyner')
        solo_form.find_element(By.CSS_SELECTOR, '.submit-row input').click()

        # he adds a solo with track and album thats not exist
        self.browser.find_element(By.LINK_TEXT, 'ADD SOLO').click()
        solo_form = self.browser.find_element(By.ID, 'solo_form')
        solo_form.find_element(By.ID, 'add_id_track').click()

        # switch to track wind
        self.browser.switch_to.window(self.browser.window_handles[1])
        track_form = self.browser.find_element(By.ID, 'track_form')
        track_form.find_element(By.NAME, 'name').send_keys('In Walked Bud')

        # add new album
        track_form.find_element(By.ID, 'add_id_album').click()
        # switch to album window
        self.browser.switch_to.window(self.browser.window_handles[2])
        album_form = self.browser.find_element(By.ID, 'album_form')
        album_form.find_element(By.NAME, 'name').send_keys('Misterioso')
        album_form.find_element(By.NAME, 'artist').send_keys(
            'Thelonious Monk Quartet')
        album_form.find_element(By.NAME, 'slug').send_keys('misterioso')
        album_form.find_element(By.CSS_SELECTOR, '.submit-row input').click()

        # switch to track window
        self.browser.switch_to.window(self.browser.window_handles[1])
        track_form = self.browser.find_element(By.ID, 'track_form')
        track_form.find_element(By.NAME, 'track_number').send_keys('4')
        track_form.find_element(By.NAME, 'slug').send_keys('in-walked-bud')
        track_form.find_element(By.CSS_SELECTOR, '.submit-row input').click()

        # switch to main (Solo) window
        self.browser.switch_to.window(self.browser.window_handles[0])
        solo_form = self.browser.find_element(By.ID, 'solo_form')
        solo_form.find_element(By.NAME, 'artist').send_keys('Johnny Griffin')
        solo_form.find_element(
            By.NAME, 'instrument').send_keys('Tenor Saxophone')
        solo_form.find_element(By.NAME, 'start_time').send_keys('0:59')
        solo_form.find_element(By.NAME, 'end_time').send_keys('6:21')
        solo_form.find_element(By.NAME, 'slug').send_keys('johnny-griffin')
        solo_form.find_element(By.CSS_SELECTOR, '.submit-row input').click()

        import pdb
        pdb.set_trace()

        self.assertEqual(self.browser.find_elements(By.CSS_SELECTOR, '#result_list tr')[
                         4].text, 'In Walked Bud Johnny Griffin 0:59-6:21')

        self.fail('Incomplete Test')
        # Test adding record and solos number

        # staff is in the right place because of the title
        #
        # username & password to login
        #
        # sees links to Albums, Tracks, Solos

    def tearDown(self):
        self.browser.quit()
