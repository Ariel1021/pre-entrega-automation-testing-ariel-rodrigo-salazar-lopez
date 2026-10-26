from pages.login_page import LoginPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.helpers import iniciar_sesion


def test_01_login_completo_exitoso(driver):

    # Instanciar la Page Class y abrir la página
    login_page = LoginPage(driver)
    login_page.abrir()

    # Completar y enviar el formulario
    login_page.login_completo("standard_user", "secret_sauce")

    # Validar la redirección al inventario
    WebDriverWait(driver, 10).until(
        EC.url_contains("/inventory.html")
    )

    assert "/inventory.html" in driver.current_url, (
        "ERROR: No se redirigió a /inventory.html"
    )

def test_02_login_exitoso(driver):

    login_page = LoginPage(driver)
    login_page.abrir()

    # Ejecutar cada acción individualmente
    login_page.completar_usuario("standard_user")
    login_page.completar_clave("secret_sauce")
    login_page.hacer_clic_login()

    # Verificar la redirección al inventario
    WebDriverWait(driver, 10).until(
        EC.url_contains("/inventory.html")
    )

    assert "/inventory.html" in driver.current_url

def test_03_login_con_clave_incorrecta(driver):

    login_page = LoginPage(driver)
    login_page.abrir()

    login_page.login_completo("standard_user", "clave_incorrecta")

    assert login_page.esta_error_visible()
    assert login_page.obtener_mensaje_error() == (
        "Epic sadface: Username and password do not match any user in this service"
    )


def test_04_login_con_campos_vacios(driver):

    login_page = LoginPage(driver)
    login_page.abrir()

    login_page.hacer_clic_login()

    assert login_page.esta_error_visible()
    assert login_page.obtener_mensaje_error() == (
        "Epic sadface: Username is required"
    )


def test_05_login_usuario_bloqueado(driver):
    
    login_page = LoginPage(driver)
    login_page.abrir()

    login_page.login_completo("locked_out_user", "secret_sauce")

    assert login_page.esta_error_visible()
    assert login_page.obtener_mensaje_error() == (
        "Epic sadface: Sorry, this user has been locked out."
    )
