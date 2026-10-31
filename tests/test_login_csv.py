import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from utils.datos import leer_csv_login

# Cargar datos del CSV
CASOS_LOGIN = leer_csv_login('datos/login.csv')

@pytest.mark.parametrize("usuario, clave, debe_funcionar, descripcion", CASOS_LOGIN)
def test_login_desde_csv(driver, usuario, clave, descripcion, debe_funcionar):

    #Test parametrizado que verifica el login con datos del CSV

    print(f"\n🧪 Probando: {descripcion}")
    print(f"   Usuario: {usuario}")
    print(f"   Debe funcionar: {'✅' if debe_funcionar else '❌'}")
    
    # Paso 1: Abrir página de login
    login = LoginPage(driver)
    login.abrir()

    # Paso 2: Completar credenciales
    login.completar_usuario(usuario)
    login.completar_clave(clave)
    login.hacer_clic_login()

    # Paso 3: Verificar resultado esperado
    if debe_funcionar:
        # Login exitoso: debe llegar al inventario
        assert "inventory.html" in driver.current_url

        inventory_page = InventoryPage(driver)
        titulo = inventory_page.obtener_titulo()
        assert titulo == "Products", f"Título incorrecto: {titulo}"
        print(f"   ✅ Login exitoso - llegó al inventario")
    else:
        # Login fallido: debe mostrar error
        assert login.esta_error_visible(), f"No se mostró error para {usuario}"
        mensaje_error = login.obtener_mensaje_error()
        assert len(mensaje_error) > 0, "El mensaje de error está vacío"
        print(f"   ❌ Login falló correctamente - Error: {mensaje_error}")


@pytest.mark.smoke
def test_login_usuario_valido_smoke(driver):
    """
    Test de smoke para verificar que al menos un login funciona
    """
    login_page = LoginPage(driver)
    login_page.abrir()
    login_page.login_completo("standard_user", "secret_sauce")
    
    assert "inventory.html" in driver.current_url
    print("✅ Test de smoke de login pasó correctamente")