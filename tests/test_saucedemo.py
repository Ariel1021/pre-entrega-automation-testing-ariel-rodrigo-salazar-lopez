import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.LoginPage import LoginPage

@pytest.fixture(scope='module')
def driver():
    options = Options()
    options.add_argument('--lang=es')

    driver = webdriver.Chrome(options=options)

    driver.implicitly_wait(10)

    yield driver

    driver.quit()


def test_01_login_exitoso(driver):
    # Abrir la página de login
    driver.get("https://www.saucedemo.com/")

    # Esperar a que el campo de usuario sea visible
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "user-name"))
    )

    # Hacer login utilizando Page Object Model
    login = LoginPage(driver)
    login.hacer_login("standard_user", "secret_sauce")

    # Validar la redirección al inventario
    WebDriverWait(driver, 10).until(
        EC.url_contains("/inventory.html")
    )

    assert driver.current_url.endswith("/inventory.html")

    # Validar el título de la sección
    titulo = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "title"))
    )

    assert titulo.text == "Products"

