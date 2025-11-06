import pytest
from selenium.webdriver.remote.webdriver import WebDriver

import allure

from pages.manager_page import ManagerPage
from data import data_ui

@allure.feature('Тест-кейс №02')
@allure.story('Сортировка клиентов по имени (First Name)')
@pytest.mark.ui         # UI test
@pytest.mark.medium     # Приортитет - средний
def test_sort_customers_by_first_name(driver: WebDriver) -> None:
    manager_page: ManagerPage = ManagerPage(driver)
    manager_page.open(data_ui.BASE_URL)

    manager_page.open_customers_tab()

    initial_names: list[str] = manager_page.get_customers_names()

    # Проверяем, что список не пустой и содержит более 1 элемента
    assert len(initial_names) > 1, \
        'Недостаточно клиентов для выполнения теста сортировки'

    manager_page.click_first_name_header()      # сортировка

    sorted_za_names: list[str] = manager_page.get_customers_names()
    expected_za_names: list[str] = sorted(initial_names, reverse=True)
    # Проверяем, что список отсортирован в обратном алфавитном порядке (Z-A)
    assert sorted_za_names == expected_za_names, \
        f'Имена не отсортированы в обратном алфавитном порядке (Z-A). Ожидалось {expected_za_names}, получено {sorted_za_names}'

    manager_page.click_first_name_header()      # сортировка

    sorted_az_names: list[str] = manager_page.get_customers_names()
    expected_az_names: list[str] = sorted(initial_names)
    # Проверяем, что список отсортирован в алфавитном порядке (A-Z)
    assert sorted_az_names == expected_az_names, \
        f'Имена не отсортированы в алфавитном порядке (A-Z). Ожидалось {expected_az_names}, получено {sorted_az_names}'
