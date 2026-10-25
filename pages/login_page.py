from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    # 1. IDENTIDAD DE LA PÁGINA
    # URL absoluta de la página de login; si cambia, solo toca este valor.
    URL = "https://www.saucedemo.com/"

    # 2. LOCATORS (privados y centralizados)
    # Define aquí todos los selectores; si el front cambia,
    # solo modificas estas tres tuplas.
    _USER_INPUT= (By.ID,"user-name")
    _PASS_INPUT= (By.ID,"password")
    _LOGIN_BUTTON = (By.ID,"login-button")
    _ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    #3. INYECCIÓN DE DEPENDENCIAS

    def __init__(self, driver):
        #Recibe la instancia de WebDriver (Chrome, Firefox…)
        #desde tu fixture en conftest.py.
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        
    # 4. MÉTODOS DE NAVEGACIÓN Y ACCIÓN

    def abrir(self):
        """Carga la URL de login en el navegador."""
        self.driver.get(self.URL)
        return self
    
    def completar_usuario(self, usuario: str):
        #Escribe el nombre de usuario.
        campo = self.wait.until(EC.visibility_of_element_located(self._USER_INPUT))
        # Limpia antes de escribir
        campo.clear()
        campo.send_keys(usuario)
        return self
    
    def completar_clave(self, clave: str):
        #Escribe la contraseña.
        campo = self.driver.find_element(*self._PASS_INPUT)
        campo.clear()
        campo.send_keys(clave)
        return self
    
    def hacer_clic_login(self):
        #Hace clic en el botón Login.
        self.driver.find_element(*self._LOGIN_BUTTON).click()
        return self
    
    def login_completo(self, usuario, clave):
        #Método de conveniencia para hacer login completo.
        self.completar_usuario(usuario)
        self.completar_clave(clave)
        self.hacer_clic_login()
        return self
    
    # 5. MÉTODOS DE VERIFICACIÓN (opcionales)
    def esta_error_visible(self) -> bool:
        #Comprueba si aparece un mensaje de error en la página 
        #tras un intento de login fallido.
        try:
            self.wait.until(EC.visibility_of_element_located(self._ERROR_MESSAGE))
            return True
        except:
            return False
        
    def obtener_mensaje_error(self) -> str:
        #Obtiene el texto del mensaje de error
        if self.esta_error_visible():
            return self.driver.find_element(*self._ERROR_MESSAGE).text
        return ""