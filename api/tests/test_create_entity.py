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
def test_create_entity_success(entity_service: EntityService) -> None:
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

    # Проверяем тип created_id (строка) и число ли это
    assert isinstance(created_id, str), \
        f'ID должен иметь тип строка, но имеет "{type(created_id)}"'
    assert created_id.isdigit(), \
        'ID должен содержать только цифры'

    # Получаем сущность
    created_entity: EntityResponse = entity_service.get_entity(created_id)

    # Проверяем созданную сущность
    assert created_entity.id == int(created_id), \
        f'Ожидалось, что ID будет "{created_id}", но получили "{created_entity.id}"'
    assert created_entity.title == initial_title, \
        f'Ожидалось, что заголовок будет "{initial_title}", но получили "{created_entity.title}"'
    assert created_entity.verified == initial_verified, \
        f'Ожидалось, что статус будет "{initial_verified}", но получили "{created_entity.verified}"'
    assert created_entity.important_numbers == initial_important_numbers, \
        f'Ожидалось, что числа будут "{initial_important_numbers}", но получили "{created_entity.important_numbers}"'
    assert created_entity.addition is not None, \
        'Ожидалось, что поле "addition" не будет None'
    assert created_entity.addition.additional_info == initial_addition.additional_info, \
        f'Ожидалось, что доп. информация будет "{initial_addition.additional_info}", но получили "{created_entity.addition.additional_info}"'
    assert created_entity.addition.additional_number == initial_addition.additional_number, \
        f'Ожидалось, что доп. число будет "{initial_addition.additional_number}", но получили "{created_entity.addition.additional_number}"'

    # Удаляем сущность
    entity_service.delete_entity(created_id)
