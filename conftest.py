import pytest
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
import subprocess
import os

from api.services.entity_service import EntityService

from typing import Generator, List, Callable

def pytest_configure() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

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

# Фикстура для удаления созданных сущностей
@pytest.fixture(scope='function')
def cleanup_entity() -> Callable[[str], None]:
    created_entity_ids: List[str] = []

    # Отслеживаем ID созданных сущностей
    def track_entity(entity_id: str) -> None:
        created_entity_ids.append(entity_id)

    yield track_entity

    service = EntityService()

    for entity_id in created_entity_ids:
        try:
            service.delete_entity(entity_id)
        except Exception as e:
            print(f'Ошибка при удалении сущности {entity_id}: {e}')

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
