from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.funciones_auxiliares import setup_driver

from pages.LoginPage import LoginPage


def test_login_exitoso():
    driver = setup_driver()

    try:
        # Abrir la página de login
        driver.get("https://www.saucedemo.com/")

        # Esperar a que el campo de usuario sea visible
        username_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "user-name"))
        )

        # Hacer Login
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

    finally:
        # Cerrar el navegador incluso si falla una validación
        driver.quit()


def test_catalogo_productos():
    driver = setup_driver()

    try:
        # Iniciar sesión
        driver.get("https://www.saucedemo.com/")

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "user-name"))
        ).send_keys("standard_user")

        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()

        # Esperar a que aparezca el catálogo
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "inventory_item"))
        )

        # Validar el título del catálogo
        titulo = driver.find_element(By.CLASS_NAME, "title")
        assert titulo.text == "Products"

        # Validar que haya productos visibles
        productos = driver.find_elements(By.CLASS_NAME, "inventory_item")
        assert len(productos) > 0

        # Validar la presencia del menú
        menu = driver.find_element(By.ID, "react-burger-menu-btn")
        assert menu.is_displayed()

        # Validar la presencia del selector de ordenamiento
        selector = driver.find_element(
            By.CLASS_NAME, "product_sort_container"
        )
        assert selector.is_displayed()

        # Obtener nombre y precio del primer producto
        primer_producto = productos[0]

        nombre = primer_producto.find_element(
            By.CLASS_NAME, "inventory_item_name"
        ).text

        precio = primer_producto.find_element(
            By.CLASS_NAME, "inventory_item_price"
        ).text

        print(f"\nPrimer producto: {nombre}")
        print(f"Precio: {precio}")

    finally:
        driver.quit()


def test_agregar_producto_al_carrito():
    driver = setup_driver()

    try:
        # Iniciar sesión
        driver.get("https://www.saucedemo.com/")

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "user-name"))
        ).send_keys("standard_user")

        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()

        # Esperar a que el catálogo esté visible
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.CLASS_NAME, "inventory_item")
            )
        )

        # Obtener el primer producto y su nombre
        primer_producto = driver.find_elements(
            By.CLASS_NAME, "inventory_item"
        )[0]

        nombre_esperado = primer_producto.find_element(
            By.CLASS_NAME, "inventory_item_name"
        ).text

        # Agregar el primer producto al carrito
        boton_agregar = primer_producto.find_element(
            By.CSS_SELECTOR, "button"
        )
        boton_agregar.click()

        # Verificar que el contador muestre 1
        contador = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.CLASS_NAME, "shopping_cart_badge")
            )
        )

        assert contador.text == "1"

        # Navegar al carrito
        driver.find_element(
            By.CLASS_NAME, "shopping_cart_link"
        ).click()

        # Esperar a que el producto aparezca en el carrito
        producto_carrito = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.CLASS_NAME, "cart_item")
            )
        )

        # Comprobar que sea el producto que agregamos
        nombre_carrito = producto_carrito.find_element(
            By.CLASS_NAME, "inventory_item_name"
        ).text

        assert nombre_carrito == nombre_esperado

    finally:
        driver.quit()
