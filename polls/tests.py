from django.test import TestCase

# Create your tests here.
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from django.contrib.auth.models import User
from django.test import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

class MySeleniumTests(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        opts = Options()
        cls.selenium = webdriver.Chrome(options=opts)
        cls.selenium.implicitly_wait(5)
        # Creación del superusuario
        user = User.objects.create_user("isard", "isard@isardvdi.com", "pirineus")
        user.is_superuser = True
        user.is_staff = True
        user.save()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_example(self):
        # Añadir aquí las pruebas con Selenium
        self.assertTrue(True)
