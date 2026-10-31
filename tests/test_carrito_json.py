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

@pytest.mark.parametrize(
    "nombre_producto",
    [producto["nombre"] for producto in PRODUCTOS]
)
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

def test_agregar_todos_los_productos(usuario_logueado):
    """
    Test que agrega todos los productos de una vez
    """
    inventory_page = usuario_logueado
    productos = leer_json_productos('datos/productos.json')
    
    print(f"\n🛒 Agregando {len(productos)} productos al carrito")
    
    contador_inicial = inventory_page.obtener_contador_carrito()
    
    for i, producto in enumerate(productos, 1):
        nombre_producto = producto['nombre']
        print(f"   {i}. Agregando: {nombre_producto}")
        
        inventory_page.agregar_producto_por_nombre(nombre_producto)
        contador_actual = inventory_page.obtener_contador_carrito()
        
        assert contador_actual == contador_inicial + i, \
            f"Contador incorrecto después de agregar {nombre_producto}"
    
    print(f"   ✅ Todos los productos agregados. Total en carrito: {contador_actual}")

@pytest.mark.smoke  
def test_carrito_smoke(usuario_logueado):
    """
    Test de smoke que verifica funcionalidad básica del carrito
    """
    inventory_page = usuario_logueado
    
    # Agregar primer producto disponible
    inventory_page.agregar_primer_producto()
    
    # Verificar que el carrito tiene 1 item
    contador = inventory_page.obtener_contador_carrito()
    assert contador == 1
    
    print("✅ Test de smoke de carrito pasó correctamente")