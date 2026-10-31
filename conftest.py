import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# function permite que se ejecute en cada función
@pytest.fixture(scope="function")
def driver():
    #Fixture que proporciona un WebDriver configurado.
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    # Para CI/CD
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False
    }
    chrome_options.add_experimental_option("prefs", prefs)


    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.maximize_window()
    driver.implicitly_wait(1)

    yield driver

    # Para ver el resultado final
    time.sleep(1)
    driver.quit()