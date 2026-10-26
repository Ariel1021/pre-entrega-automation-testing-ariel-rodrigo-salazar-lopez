from pages.login_page import LoginPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def iniciar_sesion(driver):

    login_page = LoginPage(driver)
    login_page.abrir()

    # Completar y enviar el formulario
    login_page.login_completo("standard_user", "secret_sauce")

    # Validar la redirección al inventario
    WebDriverWait(driver, 10).until(
        EC.url_contains("/inventory.html")
    )