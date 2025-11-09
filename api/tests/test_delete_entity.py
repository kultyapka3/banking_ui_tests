import pytest
import requests # Импортируем requests для проверки HTTPError

import allure

from api.services.entity_service import EntityService
from api.models.entity import EntityRequest

@allure.feature('API Entity Management')
@allure.story('Delete Entity')
@allure.title('ТС05: Удаление сущности (DELETE /api/delete/{id})')
@allure.description('''
Тест проверяет возможность удаления существующей сущности через эндпоинт DELETE /api/delete/{id}
- Создаётся тестовая сущность
- Проверяется её существование через GET /api/get/{id}
- Отправляется DELETE-запрос на /api/delete/{id}
- Отправляется GET-запрос на /api/get/{id}
- Проверяется, что запрос завершается с ошибкой (500)
''')
@allure.parent_suite('API Тесты')
@allure.suite('Positive Tests')
@pytest.mark.api        # API test
@pytest.mark.high       # Приортитет - высокий
def test_delete_entity_success(entity_service: EntityService):
    initial_title = 'delete entity'
    entity_data = EntityRequest(
        title=initial_title,
        verified=False,
        important_numbers=[]
    )

    # Создаём сущность
    created_id = entity_service.create_entity(entity_data)

    # Получаем сущность
    entity = entity_service.get_entity(created_id)

    # Проверяем созданную сущность
    assert entity.id == int(created_id), \
        f'Ожидалось, что ID будет "{created_id}", но получили "{entity.id}"'

    # Удаляем сущность
    entity_service.delete_entity(created_id)

    # Пытаемся получить удаленную сущность
    with pytest.raises(requests.HTTPError) as exc_info:
        entity_service.get_entity(created_id)
    # Проверяем, что статус ошибки соответствует удалению
    assert exc_info.value.response.status_code == 500, \
        f'Ожидалось, что код будет "500", но получили "{exc_info.value.response.status_code}"'
