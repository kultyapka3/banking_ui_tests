import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope='function')
def driver():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.page_load_strategy = 'eager'

    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()
