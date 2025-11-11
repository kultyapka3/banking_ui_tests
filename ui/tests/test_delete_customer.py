import pytest
from selenium.webdriver.remote.webdriver import WebDriver

import allure

from ui.pages.manager_page import ManagerPage
from ui.utils.list_calculator import calculate_average_length, find_name_closest_to_average
from data import data_ui

@allure.feature('Banking App Manager Actions')
@allure.story('Customers List')
@allure.title('TC03: Удаление клиента с именем, длина которого ближе всего к средней')
@allure.description('''
Тест проверяет удаление клиента, чья длина имени ближе всего к средней длине всех имён в таблице:
- Вычисляется средняя длина имён
- Определяется имя с минимальной разницей от средней длины
- Клиент удаляется, проверяется его отсутствие в таблице
''')
@allure.parent_suite('UI Тесты')
@allure.suite('Positive Tests')
@pytest.mark.ui         # UI test
@pytest.mark.high       # Приортитет - высокий
def test_delete_customer_with_average_name_length(driver: WebDriver) -> None:
    manager_page: ManagerPage = ManagerPage(driver)
    manager_page.open(data_ui.BASE_URL)

    manager_page.open_customers_tab()

    names_list: list[str] = manager_page.get_customers_names()

    # Проверяем, что список не пустой и содержит более одного элемента для вычислений
    assert len(names_list) > 1, \
        'Недостаточно клиентов для выполнения вычисления средней длины и теста удаления'

    avg_length: float = calculate_average_length(names_list)
    target_name: str = find_name_closest_to_average(names_list, avg_length)

    manager_page.delete_customer_by_name(target_name)

    updated_names_list: list[str] = manager_page.get_customers_names()
    # Проверка наличия удаленного клиента
    assert target_name not in updated_names_list, \
        f'Клиент "{target_name}" был найден в таблице после удаления.'
