from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By


class StudentTestCase(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(2)

    def test_student_find_solos(self):
        """
        test that a user can search for solos
        """
        # Steve example write todo later
        home_page = self.browser.get(self.live_server_url + '/')
        brand_element = self.browser.find_element(
            By.CLASS_NAME, 'navbar-brand')
        self.assertEqual('JMAD', brand_element.text)
        self.fail('Incomplete Test')

    def tearDown(self):
        self.browser.quit()
