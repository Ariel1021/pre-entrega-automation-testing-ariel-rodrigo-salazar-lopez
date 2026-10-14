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


def test_03_productos_visibles(driver):

    # Inicio de sesión
    iniciar_sesion(driver)

    # Obtener los productos del inventario
    inventory_items = WebDriverWait(driver, 10).until(
        EC.visibility_of_all_elements_located(
            (By.CLASS_NAME, "inventory_item")
        )
    )

    # Verificar que haya productos visibles
    assert len(inventory_items) > 0, (
        "ERROR: No se encontraron productos visibles en el inventario"
    )


def test_04_validar_interfaz(driver):
    # Inicio de sesión
    iniciar_sesion(driver)

    # Esperar a que el botón del menú sea visible
    menu_button = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.ID, "react-burger-menu-btn")
        )
    )

    # Esperar a que el filtro de ordenamiento sea visible
    filtro = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.CLASS_NAME, "product_sort_container")
        )
    )

    # Validar que ambos elementos estén visibles
    assert menu_button.is_displayed(), (
        "ERROR: El botón del menú no está visible"
    )

    assert filtro.is_displayed(), (
        "ERROR: El filtro de ordenamiento no está visible"
    )


def test_05_anadir_producto_al_carrito(driver):
    # Inicio de sesión
    iniciar_sesion(driver)

    # Obtener el primer producto
    first_item = WebDriverWait(driver, 10).until(
        EC.visibility_of_all_elements_located(
            (By.CLASS_NAME, "inventory_item")
        )
    )[0]

    # Obtener y pulsar el botón para agregarlo al carrito
    boton_agregar = first_item.find_element(By.TAG_NAME, "button")
    boton_agregar.click()

    # Esperar a que el botón cambie a "Remove"
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, ".inventory_item button"),
            "Remove"
        )
    )

    # Volver a obtener el botón y validar el cambio
    boton_agregar = first_item.find_element(By.TAG_NAME, "button")

    # Validar que el boton haya cambiado a Remove
    assert boton_agregar.text == "Remove", (
        'ERROR: El botón no cambió a "Remove"'
    )


def test_06_verificar_contador_carrito(driver):
    # Inicio de sesión
    iniciar_sesion(driver)

    # Agregar el primer producto al carrito
    first_item = WebDriverWait(driver, 10).until(
        EC.visibility_of_all_elements_located(
            (By.CLASS_NAME, "inventory_item")
        )
    )[0]

    boton_agregar = first_item.find_element(By.TAG_NAME, "button")
    boton_agregar.click()

    # Esperar a que aparezca el contador del carrito
    contador_carrito = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.CLASS_NAME, "shopping_cart_badge")
        )
    )

    # Validar que el contador sea 1
    assert contador_carrito.text == "1", (
        f"ERROR: Se esperaba 1, se obtuvo {contador_carrito.text}"
    )
