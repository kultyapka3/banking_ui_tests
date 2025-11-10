import pytest
import allure

from typing import List

from api.services.entity_service import EntityService
from api.models.entity import EntityRequest, EntityResponse

@allure.feature('API Entity Management')
@allure.story('Get All Entities')
@allure.title('ТС03: Получение списка сущностей (GET /api/getAll)')
@allure.description('''
Тест проверяет возможность получения списка всех сущностей через эндпоинт GET /api/getAll
- Создаются несколько тестовых сущностей
- Отправляется GET-запрос на /api/getAll
- Проверяется, что возвращаемый массив содержит все созданные сущности
- Сущности удаляются
''')
@allure.parent_suite('API Тесты')
@allure.suite('Positive Tests')
@pytest.mark.api        # API test
@pytest.mark.high       # Приортитет - высокий
def test_get_all_entities_success(entity_service: EntityService) -> None:
    titles: List[str] = ['get all entities1', 'get all entities2']
    created_ids: List[str] = []

    for title in titles:
        entity_data: EntityRequest = EntityRequest(title=title, verified=True, important_numbers=[10])
        created_id: str = entity_service.create_entity(entity_data)     # cоздаём сущность
        created_ids.append(created_id)                                  # записываем id сущности

    # Получаем все сущности
    all_entities: List[EntityResponse] = entity_service.get_all_entities()

    # Записываем найденные ID
    found_ids: set[int] = {e.id for e in all_entities}
    # Проверяем есть ли созданные сущности
    assert all(int(id) in found_ids for id in created_ids), \
        f'Ожидалось, что ID будут "{created_ids}", но получили "{found_ids}"'

    # Удаляем сущности
    for created_id in created_ids:
        entity_service.delete_entity(created_id)
