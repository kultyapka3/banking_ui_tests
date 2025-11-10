import pytest
import allure

from typing import List

from api.services.entity_service import EntityService
from api.models.entity import EntityRequest, EntityResponse

@allure.feature('API Entity Management')
@allure.story('Get Entity')
@allure.title('ТС02: Получение сущности (GET /api/get/{id})')
@allure.description('''
Тест проверяет возможность получения существующей сущности по её ID через эндпоинт GET /api/get/{id}
- Создаётся тестовая сущность
- Отправляется GET-запрос с ID созданной сущности
- Проверяется, что возвращаемые данные соответствуют созданным
- Сущность удаляется
''')
@allure.parent_suite('API Тесты')
@allure.suite('Positive Tests')
@pytest.mark.api        # API test
@pytest.mark.high       # Приортитет - высокий
def test_get_entity_success(entity_service: EntityService) -> None:
    initial_title: str = 'get entity'
    initial_verified: bool = False
    initial_important_numbers: List[int] = [4, 4]

    entity_data: EntityRequest = EntityRequest(
        title=initial_title,
        verified=initial_verified,
        important_numbers=initial_important_numbers
    )

    # Создаём сущность
    created_id: str = entity_service.create_entity(entity_data)

    # Получаем сущность
    retrieved_entity: EntityResponse = entity_service.get_entity(created_id)

    # Проверяем созданную сущность
    assert retrieved_entity.id == int(created_id), \
        f'Ожидалось, что ID будет "{created_id}", но получили "{retrieved_entity.id}"'
    assert retrieved_entity.title == initial_title, \
        f'Ожидалось, что заголовок будет "{initial_title}", но получили "{retrieved_entity.title}"'
    assert retrieved_entity.verified == initial_verified, \
        f'Ожидалось, что статус будет "{initial_verified}", но получили "{retrieved_entity.verified}"'
    assert retrieved_entity.important_numbers == initial_important_numbers, \
        f'Ожидалось, что числа будут "{initial_important_numbers}", но получили "{retrieved_entity.important_numbers}"'

    # Удаляем сущность
    entity_service.delete_entity(created_id)
