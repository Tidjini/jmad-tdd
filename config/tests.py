from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By

from solos.models import Solo


class StudentTestCase(LiveServerTestCase):

    INSTRUMENT_INPUT_ID = 'jmad-instrument'
    ARTIST_INPUT_ID = 'jmad-artist'

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(5)

        self.solo = Solo.objects.create(
            track='My Favorite Things',
            album='My Favorite Things',
            artist='John Coltrane',
            instrument='saxophone'
        )

        self.solo2 = Solo.objects.create(
            track='All Blues',
            album='Kind of Blue',
            start_time='2:06',
            end_time='4:01',
            artist='Canonbal Adderlay',
            instrument='saxophone'
        )

        self.solo3 = Solo.objects.create(
            track='Walts for Debby',
            artist='Canonbal Adderlay',
            instrument='saxophone',
            album='Know What I Mean?'
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
        second_artist_input.send_keys('Canonbal Adderlay')
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
                         '{}/solos/2/'.format(self.live_server_url))
        self.assertEqual(self.browser.find_element(
            By.ID, 'jmad-artist').text, 'Canonbal Adderlay')
        self.assertEqual(self.browser.find_element(
            By.ID, 'jmad-track').text, 'All Blues')
        self.assertEqual(self.browser.find_element(
            By.ID, 'jmad-album').text, 'Kind of Blue')
        # and the start time and end time of the solo
        self.assertEqual(self.browser.find_element(
            By.ID, 'jmad-start-time').text, '2:06')
        self.assertEqual(self.browser.find_element(
            By.ID, 'jmad-end-time').text, '4:01')

        self.fail('Incomplete Test')

    def tearDown(self):
        self.browser.quit()
