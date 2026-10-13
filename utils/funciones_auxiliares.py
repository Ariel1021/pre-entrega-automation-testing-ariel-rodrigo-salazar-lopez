from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


def setup_driver():
    # Configura y devuelve una instancia de Chrome WebDriver.
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service()

    driver = webdriver.Chrome(
        service=service,
        options=chrome_options
    )
    driver.maximize_window()

    return driver
