
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.helpers import iniciar_sesion


def test_01_login_exitoso(driver):

    # Abrir la página de login
    driver.get('https://www.saucedemo.com')

    # Esperar a que el campo de usuario sea visible
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "user-name"))
    )
    driver.find_element(By.ID, 'user-name').send_keys('standard_user')
    driver.find_element(By.ID, 'password').send_keys('secret_sauce')
    driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()

    # Validar inventario
    WebDriverWait(driver, 10).until(
            EC.url_contains("/inventory.html")
        )
    assert "/inventory.html" in driver.current_url, "ERROR: No se redirigió  a /inventory.html"


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

    # Valido nombre y precio del primer producto
    first_item = inventory_items[0]
    nombre = first_item.find_element(
        By.CLASS_NAME, "inventory_item_name"
    ).text

    precio = first_item.find_element(
        By.CLASS_NAME, "inventory_item_price"
    ).text

    assert nombre == 'Sauce Labs Backpack'
    assert precio == '$29.99'


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


def test_07_navegar_carrito(driver):
    # Inicio de sesión
    iniciar_sesion(driver)

    # Esperar a que el enlace del carrito sea visible
    carrito = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.CLASS_NAME, "shopping_cart_link")
        )
    )

    # Navegar al carrito
    carrito.click()

    # Esperar a que la URL cambie
    WebDriverWait(driver, 10).until(
        EC.url_contains("/cart.html")
    )

    # Validar la navegación
    assert "/cart.html" in driver.current_url, (
        "ERROR: No se redirigió a /cart.html"
    )


def test_08_comprobar_producto_en_el_carrito(driver):
    # Inicio de sesión
    iniciar_sesion(driver)

    # Obtener el primer producto del inventario
    first_item = WebDriverWait(driver, 10).until(
        EC.visibility_of_all_elements_located(
            (By.CLASS_NAME, "inventory_item")
        )
    )[0]

    # Obtener el nombre del producto seleccionado
    producto_seleccionado = first_item.find_element(
        By.CLASS_NAME, "inventory_item_name"
    ).text

    # Agregar el producto al carrito
    boton_agregar = first_item.find_element(By.TAG_NAME, "button")
    boton_agregar.click()

    # Navegar al carrito
    carrito = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.CLASS_NAME, "shopping_cart_link")
        )
    )
    carrito.click()

    # Obtener el nombre del producto en el carrito
    producto_en_carrito = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.CLASS_NAME, "inventory_item_name")
        )
    ).text

    # Comparar ambos nombres
    assert producto_en_carrito == producto_seleccionado, (
        f"ERROR: El producto del carrito ('{producto_en_carrito}') "
        f"no coincide con el seleccionado ('{producto_seleccionado}')"
    )
