from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

class BasePage:
    def __init__(self, driver, default_timeout=10):
        self.driver = driver
        self.default_timeout = default_timeout
        self.wait = WebDriverWait(driver, default_timeout)

    # Открываем URL
    def open(self, url):
        self.driver.get(url)

    # Ожидаем появление элемента в DOM
    def find_element(self, locator, timeout=None):
        timeout = timeout or self.default_timeout

        return WebDriverWait(self.driver, timeout).until(
            ec.presence_of_element_located(locator)
        )

    # Ожидаем, что элемент будет кликабелен
    def find_clickable_element(self, locator, timeout=None):
        timeout = timeout or self.default_timeout

        return WebDriverWait(self.driver, timeout).until(
            ec.element_to_be_clickable(locator)
        )

    # Кликаем по элементу
    def click_element(self, locator):
        element = self.find_clickable_element(locator)
        element.click()

    # Вводим текст в поле
    def send_keys_to_element(self, locator, text):
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    # Ожидаем появление алерта
    def wait_for_alert(self, timeout=None):
        timeout = timeout or self.default_timeout

        return WebDriverWait(self.driver, timeout).until(
            ec.alert_is_present()
        )

    # Получаем текст из алерта
    def get_alert_text(self):
        alert = self.wait_for_alert()

        return alert.text

    # Ожидаем, что элементы появятся в DOM
    def wait_for_elements_to_be_present(self, locator, timeout=None):
        timeout = timeout or self.default_timeout

        return WebDriverWait(self.driver, timeout).until(
            ec.presence_of_all_elements_located(locator)
        )

    # Ищем элементы по локатору и возвращаем их список
    def find_elements(self, locator):
        return self.driver.find_elements(*locator)
