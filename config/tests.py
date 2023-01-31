from django.test import LiveServerTestCase
from selenium import webdriver


class StudentTestCase(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(2)

    def test_student_find_solos(self):
        """
        test that a user can search for solos
        """
        # Steve example write todo later
        self.fail('Incomplete Test')

    def tearDown(self):
        self.browser.quit()
