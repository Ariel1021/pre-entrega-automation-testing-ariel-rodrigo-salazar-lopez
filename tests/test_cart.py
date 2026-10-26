from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.helpers import iniciar_sesion

def test_01_verificar_contador_carrito(driver):
    iniciar_sesion(driver)
    inventory_page = InventoryPage(driver)

    inventory_page.agregar_primer_producto()
    inventory_page.esperar_contador_carrito()

    contador = inventory_page.obtener_contador_carrito()

    assert contador == 1, (
        f"ERROR: Se esperaba 1, se obtuvo {contador}"
    )

def test_02_navegar_carrito(driver):
    iniciar_sesion(driver)
    inventory_page = InventoryPage(driver)

    inventory_page.ir_al_carrito()
    # Validar la redirección al inventario
    WebDriverWait(driver, 10).until(
        EC.url_contains("/cart.html")
    )

    assert "/cart.html" in driver.current_url, (
        "ERROR: No se redirigió a /cart.html"
    )


def test_08_comprobar_producto_en_el_carrito(driver):

    iniciar_sesion(driver)
    inventory_page = InventoryPage(driver)

    # Obtener el nombre del producto seleccionado
    productos = inventory_page.obtener_productos()
    producto_seleccionado = inventory_page.obtener_nombre_producto(
        productos[0]
    )

    # Agregarlo y navegar al carrito
    inventory_page.agregar_primer_producto()
    inventory_page.ir_al_carrito()
    
    cart_page = CartPage(driver)

    # Obtener los nombres de los productos del carrito
    nombres_carrito = cart_page.obtener_nombres_productos()

    assert producto_seleccionado in nombres_carrito, (
        f"ERROR: El producto '{producto_seleccionado}' "
        f"no aparece en el carrito: {nombres_carrito}"
    )
