from selenium.webdriver.remote.webdriver import WebDriver

import allure

from ui.pages.base_page import BasePage
from ui.pages.manager_page_locators import ManagerPageLocators

class ManagerPage(BasePage):
    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    @allure.step('Открытие страницы')
    def open(self, url: str) -> None:
        super().open(url)

    @allure.step('Переход во вкладку Add Customer')
    def open_add_customer_tab(self) -> 'ManagerPage':
        self.click_element(ManagerPageLocators.ADD_CUSTOMER_TAB_BUTTON)

        return self

    @allure.step('Добавление клиента (customer)')
    def add_customer(self, first_name: str, last_name: str, post_code: str) -> 'ManagerPage':
        self.send_keys_to_element(ManagerPageLocators.FIRST_NAME_INPUT, first_name)
        self.send_keys_to_element(ManagerPageLocators.LAST_NAME_INPUT, last_name)
        self.send_keys_to_element(ManagerPageLocators.POST_CODE_INPUT, post_code)
        self.click_element(ManagerPageLocators.ADD_CUSTOMER_BUTTON)

        return self

    @allure.step('Получение текста из алерта')
    def get_alert_text(self) -> str:
        return super().get_alert_text()

    @allure.step('Проверка наличия добавленного клиента')
    def is_customer_in_table(self, first_name: str) -> bool:
        names_in_table = self.get_customers_names()

        return first_name in names_in_table

    @allure.step('Переход во вкладку Customers')
    def open_customers_tab(self) -> 'ManagerPage':
        self.click_element(ManagerPageLocators.CUSTOMERS_TAB_BUTTON)

        return self

    @allure.step('Сортировка по имени при нажатии на First Name')
    def click_first_name_header(self) -> 'ManagerPage':
        self.click_element(ManagerPageLocators.FIRST_NAME_HEADER)

        return self

    @allure.step('Получение списка имен клиентов')
    def get_customers_names(self) -> list[str]:
        self.wait_for_elements_to_be_present(ManagerPageLocators.CUSTOMER_TABLE_ROWS)
        customers_table_rows = self.find_elements(ManagerPageLocators.CUSTOMER_TABLE_ROWS)
        names = []

        for row in customers_table_rows:
            name_element = row.find_element(*ManagerPageLocators.CUSTOMER_TABLE_FIRST_NAME_CELL)
            raw_name_text = name_element.text
            name = raw_name_text.strip()

            if name:
                names.append(name)

        return names

    @allure.step('Удаление выбранного клиента')
    def delete_customer_by_name(self, target_name: str) -> None:
        self.wait_for_elements_to_be_present(ManagerPageLocators.CUSTOMER_TABLE_ROWS)
        customers_table_rows = self.find_elements(ManagerPageLocators.CUSTOMER_TABLE_ROWS)

        for row in customers_table_rows:
            name_cell = row.find_element(*ManagerPageLocators.CUSTOMER_TABLE_FIRST_NAME_CELL)

            if name_cell.text == target_name:
                delete_button = row.find_element(*ManagerPageLocators.DELETE_BUTTON)
                delete_button.click()

                break
        else:
            raise ValueError(f'Клиент "{target_name}" не был найден в таблице')
