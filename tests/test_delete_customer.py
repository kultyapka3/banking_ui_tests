import pytest
import allure

from pages.manager_page import ManagerPage
from utils.list_calculator import calculate_average_length, find_name_closest_to_average
from utils import config

@allure.feature('Тест-кейс №03')
@allure.story('Удаление клиента с именем, длина которого ближе всего к средней')
@pytest.mark.ui         # UI test
@pytest.mark.high       # Приортитет - высокий
def test_delete_customer_with_average_name_length(driver):
    manager_page = ManagerPage(driver)
    manager_page.open(config.BASE_URL)

    manager_page.open_customers_tab()

    names_list = manager_page.get_customers_names()

    # Проверяем, что список не пустой и содержит более одного элемента для вычислений
    assert len(names_list) > 1, \
        'Недостаточно клиентов для выполнения вычисления средней длины и теста удаления'

    avg_length = calculate_average_length(names_list)
    target_name = find_name_closest_to_average(names_list, avg_length)

    manager_page.delete_customer_by_name(target_name)

    updated_names_list = manager_page.get_customers_names()
    # Проверка наличия удаленного клиента
    assert target_name not in updated_names_list, \
        f'Клиент "{target_name}" был найден в таблице после удаления.'
