from pages.inventory_page import InventoryPage
from utils.helpers import iniciar_sesion


def test_01_verificar_inventario(driver):

    iniciar_sesion(driver)

    inventory_page = InventoryPage(driver)

    # Validar título de la ventana
    page_title = inventory_page.obtener_titulo_ventana()
    assert page_title == "Swag Labs", (
        f'ERROR: Título esperado "Swag Labs", obtenido "{page_title}"'
    )

    # Validar título de la sección
    section_title = inventory_page.obtener_titulo()
    assert section_title == "Products", (
        f'ERROR: Título de sección esperado "Products", '
        f'obtenido "{section_title}"'
    )


def test_02_productos_visibles(driver):
    iniciar_sesion(driver)
    inventory_page = InventoryPage(driver)

    # Obtener los productos
    productos = inventory_page.obtener_productos()

    # Verificar que haya productos
    assert len(productos) > 0, (
        "ERROR: No se encontraron productos en el inventario"
    )

    # Validar nombre y precio del primer producto
    primer_producto = productos[0]

    nombre = inventory_page.obtener_nombre_producto(primer_producto)
    precio = inventory_page.obtener_precio_producto(primer_producto)

    assert nombre == "Sauce Labs Backpack", (
        f"ERROR: Nombre esperado 'Sauce Labs Backpack', obtenido '{nombre}'"
    )
    assert precio == "$29.99", (
        f"ERROR: Precio esperado '$29.99', obtenido '{precio}'"
    )

def test_03_validar_interfaz(driver):
    iniciar_sesion(driver)
    inventory_page = InventoryPage(driver)

    assert inventory_page.menu_visible(), (
        "ERROR: El botón del menú no está visible"
    )

    assert inventory_page.filtro_ordenamiento_visible(), (
        "ERROR: El filtro de ordenamiento no está visible"
    )
