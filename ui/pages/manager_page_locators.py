from selenium.webdriver.common.by import By

from typing import Tuple

# Тип локатора для аннотаций
Locator = Tuple[By, str]

class ManagerPageLocators:
    # Навигация
    ADD_CUSTOMER_TAB_BUTTON: Locator = (By.CSS_SELECTOR, 'button[ng-click="addCust()"]')
    CUSTOMERS_TAB_BUTTON: Locator = (By.CSS_SELECTOR, 'button[ng-click="showCust()"]')

    # Вкладка Add Customer
    FIRST_NAME_INPUT: Locator = (By.CSS_SELECTOR, '[ng-model="fName"]')
    LAST_NAME_INPUT: Locator = (By.CSS_SELECTOR, '[ng-model="lName"]')
    POST_CODE_INPUT: Locator = (By.CSS_SELECTOR, '[ng-model="postCd"]')
    ADD_CUSTOMER_BUTTON: Locator = (By.CSS_SELECTOR, 'button[type="submit"]')

    # Вкладка Customers
    CUSTOMER_TABLE_ROWS: Locator = (By.XPATH, '//table[contains(@class, "table")]//tbody/tr')
    FIRST_NAME_HEADER: Locator = (By.XPATH, "//a[@ng-click=\"sortType = 'fName'; sortReverse = !sortReverse\"]")
    DELETE_BUTTON: Locator = (By.XPATH, './/button[@ng-click=\"deleteCust(cust)\"]')
    CUSTOMER_TABLE_FIRST_NAME_CELL: Locator = (By.XPATH, './/td[1]')