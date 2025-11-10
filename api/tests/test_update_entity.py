import pytest
import allure

from typing import List

from api.services.entity_service import EntityService
from api.models.entity import EntityRequest, AdditionRequest, EntityResponse

@allure.feature('API Entity Management')
@allure.story('Update Entity')
@allure.title('ТС04: Обновление сущности (PATCH /api/patch/{id})')
@allure.description('''
Тест проверяет возможность обновления существующей сущности через эндпоинт PATCH /api/patch/{id}
- Создаётся тестовая сущность
- Отправляется PATCH-запрос с новыми данными для созданной сущности
- Отправляется GET-запрос на /api/get/{id}
- Проверяется, что возвращаемые данные содержат обновлённые значения (с учётом поведения API)
- Сущность удаляется
''')
@allure.parent_suite('API Тесты')
@allure.suite('Positive Tests')
@pytest.mark.api        # API test
@pytest.mark.high       # Приортитет - высокий
def test_update_entity_success(entity_service: EntityService) -> None:
    initial_title: str = 'update entity'
    initial_verified: bool = False
    initial_important_numbers: List[int] = [777, 777]
    initial_addition: AdditionRequest = AdditionRequest(additional_info='update additional', additional_number=777)

    entity_data: EntityRequest = EntityRequest(
        title=initial_title,
        verified=initial_verified,
        important_numbers=initial_important_numbers,
        addition=initial_addition
    )

    # Создаём сущность
    created_id: str = entity_service.create_entity(entity_data)

    # Получаем сущность
    initial_entity: EntityResponse = entity_service.get_entity(created_id)
    # Проверяем созданную сущность
    assert initial_entity.title == initial_title, \
        f'Ожидалось, что заголовок будет "{initial_title}", но получили "{initial_entity.title}"'
    assert initial_entity.verified == initial_verified, \
        f'Ожидалось, что статус будет "{initial_verified}", но получили "{initial_entity.verified}"'

    updated_title: str = 'successful update entity'
    updated_verified: bool = True
    updated_important_numbers: List[int] = [666, 666]
    updated_addition: AdditionRequest = AdditionRequest(additional_info='updated additional', additional_number=666)

    update_data: EntityRequest = EntityRequest(
        title=updated_title,
        verified=updated_verified,
        important_numbers=updated_important_numbers,
        addition=updated_addition
    )

    # Обновляем сущность
    entity_service.update_entity(created_id, update_data)

    # Получаем обновленную сущность
    updated_entity: EntityResponse = entity_service.get_entity(created_id)

    # Проверяем обновленную сущность
    assert updated_entity.id == int(created_id), \
        f'Ожидалось, что ID будет "{created_id}", но получили "{updated_entity.id}"'
    assert updated_entity.title == updated_title, \
        f'Ожидалось, что заголовок будет "{updated_title}", но получили "{updated_entity.title}"'
    assert updated_entity.verified == updated_verified, \
        f'Ожидалось, что статус будет "{updated_verified}", но получили "{updated_entity.verified}"'
    assert updated_entity.important_numbers == updated_important_numbers, \
        f'Ожидалось, что числа будут "{updated_important_numbers}", но получили "{updated_entity.important_numbers}"'
    assert updated_entity.addition is not None, \
        'Ожидалось, что поле "addition" не будет None'
    assert updated_entity.addition.additional_info == updated_addition.additional_info, \
        f'Ожидалось, что доп. информация будет "{updated_addition.additional_info}", но получили "{updated_entity.addition.additional_info}"'
    assert updated_entity.addition.additional_number == updated_addition.additional_number, \
        f'Ожидалось, что доп. число будет "{updated_addition.additional_number}", но получили "{updated_entity.addition.additional_number}"'

    # Удаляем сущность
    entity_service.delete_entity(created_id)
