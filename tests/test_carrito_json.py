import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from utils.datos import leer_json_productos

# Cargar productos desde JSON
PRODUCTOS = leer_json_productos('datos/productos.json')

@pytest.fixture
def usuario_logueado(driver):
    """
    Fixture que realiza login antes de cada test de carrito
    """
    login_page = LoginPage(driver)
    login_page.abrir()
    login_page.login_completo("standard_user", "secret_sauce")
    
    # Verificar que el login fue exitoso
    assert "inventory.html" in driver.current_url
    
    return InventoryPage(driver)

@pytest.mark.parametrize("nombre_producto", PRODUCTOS)
def test_agregar_producto_desde_json(usuario_logueado, nombre_producto):
    """
    Test que agrega cada producto del JSON al carrito
    """
    inventory_page = usuario_logueado
    
    print(f"\n🛒 Agregando producto: {nombre_producto}")
    
    # Obtener contador inicial del carrito
    contador_inicial = inventory_page.obtener_contador_carrito()
    print(f"   Contador inicial: {contador_inicial}")
    
    # Agregar producto específico
    inventory_page.agregar_producto_por_nombre(nombre_producto)
    
    # Verificar que el contador se incrementó
    contador_final = inventory_page.obtener_contador_carrito()
    print(f"   Contador final: {contador_final}")
    
    assert contador_final == contador_inicial + 1, \
        f"El contador no se incrementó correctamente para {nombre_producto}"
    
    print(f"   ✅ Producto agregado correctamente")