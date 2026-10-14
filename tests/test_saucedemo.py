import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.LoginPage import LoginPage

def iniciar_sesion(driver):
    # Abrir la página de login
    driver.get("https://www.saucedemo.com/")

    # Esperar a que el campo de usuario sea visible
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "user-name"))
    )

    # Hacer login 
    login = LoginPage(driver)
    login.hacer_login("standard_user", "secret_sauce")

    WebDriverWait(driver, 10).until(
        EC.url_contains("/inventory.html")
    )

@pytest.fixture()
def driver():
    options = Options()
    options.add_argument('--lang=es')

    driver = webdriver.Chrome(options=options)

    driver.implicitly_wait(10)

    yield driver

    driver.quit()


def test_01_login_exitoso(driver):

    # Inicio de sesión
    iniciar_sesion(driver)

    # Validar el título de la sección
    titulo = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "title"))
    )

    # Validar título de la sección
    assert titulo.text == "Products"


def test_02_verificar_inventario(driver):

    # Inicio de sesión
    iniciar_sesion(driver)

    # Validar título de la página
    page_title = driver.title
    assert page_title == "Swag Labs", (
        f'ERROR: Título de ventana esperado "Swag Labs", '
        f'obtenido "{page_title}"'
    )

    # Validar título de la sección
    titulo = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "title"))
    )
    section_title = titulo.text
    assert section_title == "Products", (
        f'ERROR: Título de sección esperado "Products", '
        f'obtenido "{section_title}"'
    )
