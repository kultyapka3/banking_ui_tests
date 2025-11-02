import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import subprocess
import os

@pytest.fixture(scope='function')
def driver():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.page_load_strategy = 'eager'

    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()

# Хук для генерации отчетов Allure
@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
    # Запускаем только в локальной среде
    if os.getenv("CI"):
        return

    # Если процесс не главный, то не запускаем
    if hasattr(session.config, 'workerinput'):
        return

    allure_results_dir = session.config.getoption('--alluredir')
    subprocess.Popen(['allure.bat', 'serve', allure_results_dir], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
