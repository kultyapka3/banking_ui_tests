from selenium.webdriver.common.by import By

class ManagerPageLocators:
    # Навигация
    ADD_CUSTOMER_TAB_BUTTON = (By.CSS_SELECTOR, 'button[ng-click="addCust()"]')
    CUSTOMERS_TAB_BUTTON = (By.CSS_SELECTOR, 'button[ng-click="showCust()"]')

    # Вкладка Add Customer
    FIRST_NAME_INPUT = (By.CSS_SELECTOR, '[ng-model="fName"]')
    LAST_NAME_INPUT = (By.CSS_SELECTOR, '[ng-model="lName"]')
    POST_CODE_INPUT = (By.CSS_SELECTOR, '[ng-model="postCd"]')
    ADD_CUSTOMER_BUTTON = (By.CSS_SELECTOR, 'button[type="submit"]')

    # Вкладка Customers
    CUSTOMER_TABLE_ROWS = (By.XPATH, '//table[contains(@class, "table")]//tbody/tr')
    FIRST_NAME_HEADER = (By.XPATH, "//a[@ng-click=\"sortType = 'fName'; sortReverse = !sortReverse\"]")
    DELETE_BUTTON = (By.XPATH, './/button[@ng-click=\"deleteCust(cust)\"]')
    CUSTOMER_TABLE_FIRST_NAME_CELL = (By.XPATH, './/td[1]')