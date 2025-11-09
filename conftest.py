import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
import subprocess
import os

from api.services.entity_service import EntityService

from typing import Generator

# Фикстура для UI тестов (веб-драйвер)
@pytest.fixture(scope='function')
def driver() -> Generator[WebDriver, None, None]:
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.page_load_strategy = 'eager'

    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()

# Фикстура для API тестов (EntityService)
@pytest.fixture(scope='function')
def entity_service() -> Generator[EntityService, None, None]:
    service = EntityService()
    yield service

# Хук для генерации отчетов Allure
@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus) -> None:
    # Запускаем только в локальной среде
    if os.getenv('CI'):
        return

    # Если процесс не главный, то не запускаем
    if hasattr(session.config, 'workerinput'):
        return

    allure_results_dir = session.config.getoption('--alluredir')
    subprocess.Popen(['allure.bat', 'serve', allure_results_dir], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
