import pytest
from selenium.webdriver.remote.webdriver import WebDriver

import allure

from pages.manager_page import ManagerPage
from utils.data_generator import generate_post_code, post_code_to_first_name
from data import data_ui

@allure.feature('Тест-кейс №01')
@allure.story('Создание клиента с генерацией данных (Add Customer)')
@pytest.mark.ui         # UI test
@pytest.mark.high       # Приортитет - высокий
def test_add_customer_with_generated_data(driver: WebDriver) -> None:
    post_code: str = generate_post_code(length=10)
    first_name: str = post_code_to_first_name(post_code)
    last_name: str = 'Test'

    manager_page: ManagerPage = ManagerPage(driver)
    manager_page.open(data_ui.BASE_URL)

    manager_page.open_add_customer_tab() \
                .add_customer(first_name, last_name, post_code)

    alert_text: str = manager_page.get_alert_text()
    expected_alert_part: str = 'Customer added successfully'
    driver.switch_to.alert.accept()
    # Проверяем содержание алерта
    assert expected_alert_part in alert_text, \
        f'Ожидалось, что текст алерта будет содержать "{expected_alert_part}", но получили "{alert_text}"'

    manager_page.open_customers_tab()
    # Проверяем, появился ли клиент в таблице
    assert manager_page.is_customer_in_table(first_name), \
        f'Клиент "{first_name}" не был найден в таблице после его добавления'
