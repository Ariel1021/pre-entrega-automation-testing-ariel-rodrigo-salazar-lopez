from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def iniciar_sesion(driver):

    # Abrir la página de login
    driver.get('https://www.saucedemo.com')

    # Esperar a que el campo de usuario sea visible
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "user-name"))
    )
    driver.find_element(By.ID, 'user-name').send_keys('standard_user')
    driver.find_element(By.ID, 'password').send_keys('secret_sauce')
    driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()