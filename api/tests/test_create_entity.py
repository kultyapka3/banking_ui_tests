import pytest
import allure

from typing import List

from api.services.entity_service import EntityService
from api.models.entity import EntityRequest, AdditionRequest, EntityResponse

@allure.feature('API Entity Management')
@allure.story('Create Entity')
@allure.title('ТС01: Создание сущности (POST /api/create)')
@allure.description('''
Тест проверяет возможность создания новой сущности через эндпоинт POST /api/create
- Подготавливаются данные для создания
- Отправляется POST-запрос с этими данными
- Проверяется возвращаемый ID
- Проверяется, что созданная сущность доступна по GET /api/get/{id}
- Сущность удаляется
''')
@allure.parent_suite('API Тесты')
@allure.suite('Positive Tests')
@pytest.mark.api        # API test
@pytest.mark.high       # Приортитет - высокий
def test_create_entity_success(entity_service: EntityService, cleanup_entity) -> None:
    initial_title: str = 'create entity'
    initial_verified: bool = True
    initial_important_numbers: List[int] = [52, 52]
    initial_addition: AdditionRequest = AdditionRequest(additional_info='additional', additional_number=52)

    entity_data: EntityRequest = EntityRequest(
        title=initial_title,
        verified=initial_verified,
        important_numbers=initial_important_numbers,
        addition=initial_addition
    )

    # Создаём сущность
    created_id: str = entity_service.create_entity(entity_data)
    # Добавляем ID для автоматического удаления
    cleanup_entity(created_id)

    # Проверяем тип created_id (строка) и его содержание
    assert isinstance(created_id, str) and created_id.isdigit(), \
        f'ID должен иметь тип строка и содержать цифры, но имеет "{type(created_id)}"'

    # Получаем сущность
    created_entity: EntityResponse = entity_service.get_entity(created_id)

    # Проверяем созданную сущность по ключевому полю
    assert created_entity.title == initial_title, \
        f'Ожидалось, что заголовок будет "{initial_title}", но получили "{created_entity.title}"'
