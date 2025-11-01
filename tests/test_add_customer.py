import allure

from pages.manager_page import ManagerPage
from utils.data_generator import generate_post_code, post_code_to_first_name
from utils import config

@allure.feature('Тест-кейс №01')
@allure.story('Создание клиента с генерацией данных (Add Customer)')
def test_add_customer_with_generated_data(driver):
    post_code = generate_post_code(length=10)
    first_name = post_code_to_first_name(post_code)
    last_name = 'Test'

    manager_page = ManagerPage(driver)
    manager_page.open(config.BASE_URL)

    manager_page.open_add_customer_tab() \
                .add_customer(first_name, last_name, post_code)

    alert_text = manager_page.get_alert_text()
    expected_alert_part = 'Customer added successfully'
    driver.switch_to.alert.accept()
    # Проверяем содержание алерта
    assert expected_alert_part in alert_text, \
        f'Ожидалось, что текст алерта будет содержать "{expected_alert_part}", но получили "{alert_text}"'

    manager_page.open_customers_tab()
    # Проверяем, появился ли клиент в таблице
    assert manager_page.is_customer_in_table(first_name), \
        f'Клиент "{first_name}" не был найден в таблице после его добавления'
