from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RegistroPage:
    # Usaremos una página que realmente funciona para mostrar mensajes
    URL = "https://the-internet.herokuapp.com/forgot_password"
    
    # Locators actualizados
    _EMAIL_INPUT = (By.ID, "email")
    _SUBMIT_BUTTON = (By.ID, "form_submit")
    _SUCCESS_MESSAGE = (By.ID, "content")
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def abrir(self):
        """Navegar a la página de registro"""
        self.driver.get(self.URL)
        return self
    
    def completar_email(self, email):
        """Completar el campo email"""
        campo = self.wait.until(EC.visibility_of_element_located(self._EMAIL_INPUT))
        campo.clear()
        campo.send_keys(email)
        return self
    
    def enviar(self):
        """Hacer clic en el botón de enviar"""
        self.driver.find_element(*self._SUBMIT_BUTTON).click()
        return self
    
    def obtener_mensaje(self):
        """Obtener el mensaje de respuesta"""
        try:
            # Esperar a que aparezca el mensaje después del submit
            self.wait.until(EC.url_contains("email_sent"))
            elemento = self.driver.find_element(*self._SUCCESS_MESSAGE)
            return elemento.text
        except:
            return ""