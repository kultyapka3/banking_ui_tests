from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By

from typing import Tuple, Optional

from utils import config

# Тип локатора для аннотаций
Locator = Tuple[By, str]

class BasePage:
    def __init__(self, driver: WebDriver, default_timeout: int = config.DEFAULT_TIMEOUT):
        self.driver = driver
        self.default_timeout = default_timeout
        self.wait = WebDriverWait(driver, default_timeout)

    # Открываем URL
    def open(self, url: str) -> None:
        self.driver.get(url)

    # Ожидаем появление элемента в DOM
    def find_element(self, locator: Locator, timeout: Optional[int] = None) -> WebElement:
        timeout = timeout or self.default_timeout

        return WebDriverWait(self.driver, timeout).until(
            ec.presence_of_element_located(locator)
        )

    # Ожидаем, что элемент будет кликабелен
    def find_clickable_element(self, locator: Locator, timeout: Optional[int] = None) -> WebElement:
        timeout = timeout or self.default_timeout

        return WebDriverWait(self.driver, timeout).until(
            ec.element_to_be_clickable(locator)
        )

    # Кликаем по элементу
    def click_element(self, locator: Locator) -> None:
        element = self.find_clickable_element(locator)
        element.click()

    # Вводим текст в поле
    def send_keys_to_element(self, locator: Locator, text: str) -> None:
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    # Ожидаем появление алерта
    def wait_for_alert(self, timeout: Optional[int] = None) -> Alert:
        timeout = timeout or self.default_timeout

        return WebDriverWait(self.driver, timeout).until(
            ec.alert_is_present()
        )

    # Получаем текст из алерта
    def get_alert_text(self) -> str:
        alert = self.wait_for_alert()

        return alert.text

    # Ожидаем, что элементы появятся в DOM
    def wait_for_elements_to_be_present(self, locator: Locator, timeout: Optional[int] = None) -> list[WebElement]:
        timeout = timeout or self.default_timeout

        return WebDriverWait(self.driver, timeout).until(
            ec.presence_of_all_elements_located(locator)
        )

    # Ищем элементы по локатору и возвращаем их список
    def find_elements(self, locator: Locator) -> list[WebElement]:
        return self.driver.find_elements(*locator)
