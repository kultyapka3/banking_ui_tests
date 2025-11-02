from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

import allure

from pages.manager_page_locators import ManagerPageLocators

class ManagerPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    @allure.step('Открытие страницы')
    def open(self, url):
        self.driver.get(url)

    @allure.step('Переход во вкладку Add Customer')
    def open_add_customer_tab(self):
        add_customer_tab = self.wait.until(ec.element_to_be_clickable(ManagerPageLocators.ADD_CUSTOMER_TAB_BUTTON))
        add_customer_tab.click()

        return self

    @allure.step('Добавление клиента (customer)')
    def add_customer(self, first_name, last_name, post_code):
        first_name_field = self.wait.until(ec.presence_of_element_located(ManagerPageLocators.FIRST_NAME_INPUT))
        last_name_field = self.wait.until(ec.presence_of_element_located(ManagerPageLocators.LAST_NAME_INPUT))
        post_code_field = self.wait.until(ec.presence_of_element_located(ManagerPageLocators.POST_CODE_INPUT))
        add_customer_button = self.wait.until(ec.element_to_be_clickable(ManagerPageLocators.ADD_CUSTOMER_BUTTON))

        first_name_field.send_keys(first_name)
        last_name_field.send_keys(last_name)
        post_code_field.send_keys(post_code)
        add_customer_button.click()

        return self

    @allure.step('Получение текста из алерта')
    def get_alert_text(self):
        alert = self.wait.until(ec.alert_is_present())

        return alert.text

    @allure.step('Проверка наличия добавленного клиента')
    def is_customer_in_table(self, first_name):
        names_in_table = self.get_customers_names()

        return first_name in names_in_table

    @allure.step('Переход во вкладку Customers')
    def open_customers_tab(self):
        customers_tab = self.wait.until(ec.element_to_be_clickable(ManagerPageLocators.CUSTOMERS_TAB_BUTTON))
        customers_tab.click()

        return self

    @allure.step('Сортировка по имени при нажатии на First Name')
    def click_first_name_header(self):
        first_name_header = self.wait.until(ec.element_to_be_clickable(ManagerPageLocators.FIRST_NAME_HEADER))
        first_name_header.click()

        return self

    @allure.step('Получение списка имен клиентов')
    def get_customers_names(self):
        self.wait.until(ec.presence_of_all_elements_located(ManagerPageLocators.CUSTOMER_TABLE_ROWS))
        customers_table_rows = self.driver.find_elements(*ManagerPageLocators.CUSTOMER_TABLE_ROWS)
        names = []

        for row in customers_table_rows:
            name_element = row.find_element(*ManagerPageLocators.CUSTOMER_TABLE_FIRST_NAME_CELL)
            raw_name_text = name_element.text
            name = raw_name_text.strip()

            if name:
                names.append(name)

        return names

    @allure.step('Удаление выбранного клиента')
    def delete_customer_by_name(self, target_name):
        self.wait.until(ec.presence_of_element_located(ManagerPageLocators.CUSTOMER_TABLE_ROWS))
        customers_table_rows = self.driver.find_elements(*ManagerPageLocators.CUSTOMER_TABLE_ROWS)

        for row in customers_table_rows:
            name_cell = row.find_element(*ManagerPageLocators.CUSTOMER_TABLE_FIRST_NAME_CELL)

            if name_cell.text == target_name:
                delete_button = row.find_element(*ManagerPageLocators.DELETE_BUTTON)
                delete_button.click()
                self.driver.implicitly_wait(1)

                break
        else:
            raise ValueError(f'Клиент "{target_name}" не был найден в таблице')