from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import time

class StaffPermissionsTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        opts = Options()
        cls.selenium = WebDriver(options=opts)
        cls.selenium.implicitly_wait(5)

        # Crear superusuario en la BD directamente
        user = User.objects.create_user("isard", "isard@isardvdi.com", "pirineus")
        user.is_superuser = True
        user.is_staff = True
        user.save()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def create_staff_user(self):
        """Crea un usuario staff a través del panel de administración con Selenium"""
        self.selenium.get(f"{self.live_server_url}/admin/login/")
        username_input = self.selenium.find_element(By.NAME, "username")
        password_input = self.selenium.find_element(By.NAME, "password")

        username_input.send_keys("isard")
        password_input.send_keys("pirineus")
        password_input.send_keys(Keys.RETURN)

        self.selenium.get(f"{self.live_server_url}/admin/auth/user/add/")

        # Esperar campo de usuario
        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        ).send_keys("staff")

        # Introducir contraseña y confirmación
        self.selenium.find_element(By.NAME, "password1").send_keys("pirineus")
        self.selenium.find_element(By.NAME, "password2").send_keys("pirineus")

        # Guardar usuario
        self.selenium.find_element(By.NAME, "_save").click()
        time.sleep(2)

        # Asignar permisos de staff
        self.selenium.get(f"{self.live_server_url}/admin/auth/user/")
        WebDriverWait(self.selenium, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "staff"))
        ).click()
        self.selenium.find_element(By.NAME, "is_staff").click()
        self.selenium.find_element(By.NAME, "_save").click()
        time.sleep(2)

        # Cerrar sesión del superusuario
        self.selenium.find_element(By.XPATH, "//button[text()='Log out']")
        #self.driver.get(f"{self.live_server_url}/admin/logout/")
        time.sleep(2)

    def test_staff_cannot_access_users(self):
        """Prueba que un usuario staff no puede acceder a la gestión de usuarios"""
        self.create_staff_user()
        self.selenium.get(f"{self.live_server_url}/admin/login/")
        username_input = self.selenium.find_element(By.NAME, "username")
        password_input = self.selenium.find_element(By.NAME, "password")

        username_input.send_keys("staff")
        password_input.send_keys("pirineus")
        password_input.send_keys(Keys.RETURN)

        # Intentar acceder a /admin/auth/user/
        self.selenium.get(f"{self.live_server_url}/admin/auth/user/")
        error_message = "No tienes permisos para ver este contenido"
        self.assertIn(error_message, self.selenium.page_source)

    def test_staff_cannot_create_questions(self):
        """Prueba que un usuario staff no puede crear preguntas en polls"""
        self.selenium.get(f"{self.live_server_url}/admin/login/")
        username_input = self.selenium.find_element(By.NAME, "username")
        password_input = self.selenium.find_element(By.NAME, "password")

        username_input.send_keys("staff")
        password_input.send_keys("pirineus")
        password_input.send_keys(Keys.RETURN)

        # Intentar acceder a /admin/polls/question/add/
        self.selenium.get(f"{self.live_server_url}/admin/polls/question/add/")
        error_message = "No tienes permisos para ver este contenido"
        self.assertIn(error_message, self.selenium.page_source)
