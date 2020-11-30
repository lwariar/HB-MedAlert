from selenium import webdriver
import unittest

class TestMedAlert(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def test_title(self):
        self.browser.get('http://localhost:5000')
        self.assertEqual(self.browser.title, 'MedAlert')
