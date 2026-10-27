from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class InventoryPage:
    _TITLE = (By.CLASS_NAME, "title")
    _PRODUCTS = (By.CLASS_NAME, "inventory_item")
    _ADD_BUTTONS = (By.CSS_SELECTOR, "button[data-test*='add-to-cart']")
    _CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    _CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    _SORT_FILTER = (By.CLASS_NAME, "product_sort_container")
    _MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    _LOGOUT_LINK = (By.ID, "logout_sidebar_link")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def obtener_titulo_ventana(self):
        """Obtiene el título de la ventana del navegador."""
        return self.driver.title

    def obtener_titulo(self):
        """Obtiene el título de la página de inventario."""
        return self.driver.find_element(*self._TITLE).text
    
    def obtener_productos(self):
        """Obtiene la lista de productos disponibles."""
        return self.driver.find_elements(*self._PRODUCTS)
        
    def obtener_nombre_producto(self, producto):
        """Obtiene el nombre de un producto."""
        return producto.find_element(
            By.CLASS_NAME, "inventory_item_name"
        ).text

    def obtener_precio_producto(self, producto):
        """Obtiene el precio de un producto."""
        return producto.find_element(
            By.CLASS_NAME, "inventory_item_price"
        ).text
    
    def agregar_primer_producto(self):
        """Añade el primer producto disponible al carrito."""
        primer_boton = self.driver.find_elements(*self._ADD_BUTTONS)[0]
        primer_boton.click()
        return self
    
    def obtener_contador_carrito(self):
        """Obtiene el número de productos en el carrito."""
        try:
            badge = self.driver.find_element(*self._CART_BADGE)
            return int(badge.text)
        except:
            return 0
        
    def ir_al_carrito(self):
        """Navega a la página del carrito."""
        self.driver.find_element(*self._CART_LINK).click()
        # Importación lazy para evitar dependencias circulares
        return self

    def esperar_contador_carrito(self):
        """Espera a que aparezca el contador del carrito."""
        return self.wait.until(
            EC.visibility_of_element_located(self._CART_BADGE)
        )

    def menu_visible(self):
        """Indica si el botón del menú está visible."""
        return self.wait.until(
            EC.visibility_of_element_located(self._MENU_BUTTON)
        ).is_displayed()

    def filtro_ordenamiento_visible(self):
        """Indica si el filtro de ordenamiento está visible."""
        return self.wait.until(
            EC.visibility_of_element_located(self._SORT_FILTER)
        ).is_displayed()
    
    def hacer_logout(self):
        """Cierra la sesión del usuario."""
        self.driver.find_element(*self._MENU_BUTTON).click()
        logout_link = self.wait.until(
        EC.element_to_be_clickable(self._LOGOUT_LINK)
        )
        logout_link.click()
        from pages.login_page import LoginPage
        return LoginPage(self.driver)