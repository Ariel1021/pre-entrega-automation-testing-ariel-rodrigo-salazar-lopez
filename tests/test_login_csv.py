import pytest
from pages.login_page import LoginPage
from utils.datos import leer_csv_login

# Cargar datos del CSV
CASOS_LOGIN = leer_csv_login('datos/login.csv')

@pytest.mark.parametrize("usuario, clave, debe_funcionar", CASOS_LOGIN)
def test_login_desde_csv(driver, usuario, clave, debe_funcionar):
    login = LoginPage(driver)
    login.abrir()
    login.completar_usuario(usuario)
    login.completar_clave(clave)
    login.enviar()
    
    if debe_funcionar:
        assert "inventory.html" in driver.current_url
    else:
        assert login.hay_error()