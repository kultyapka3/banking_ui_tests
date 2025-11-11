import allure
import logging

from typing import List, Optional

from api.services.base_api import APIClient
from api.models.entity import EntityRequest, EntityResponse
from data import data_api

logger = logging.getLogger(__name__)

class EntityService(APIClient):
    def __init__(self, base_url: str = data_api.BASE_URL):
        super().__init__(base_url)
        logger.info(f'Инициализирован EntityService для {base_url}')

    @allure.step('Создание сущности')
    def create_entity(self, entity_data: EntityRequest) -> str:
        logger.info(f'Создание сущности с данными: {entity_data.model_dump()}')
        response = self.post(
            data_api.CREATE_ENDPOINT,
            json=entity_data.model_dump()
        )
        created_id = response.text
        logger.info(f'ID успешно созданной сущности: {created_id}')

        return created_id

    @allure.step('Получение сущности с ID "{entity_id}"')
    def get_entity(self, entity_id: str) -> EntityResponse:
        logger.info(f'Получение сущности с ID: {entity_id}')
        response = self.get(data_api.GET_ENDPOINT.format(id=entity_id))
        entity_data = response.json()
        logger.info(f'Получены данные сущности с ID {entity_id}')

        return EntityResponse.model_validate(entity_data)

    @allure.step('Получение всех сущностей')
    def get_all_entities(
            self,
            title: Optional[str] = None,
            verified: Optional[bool] = None,
            page: Optional[int] = None,
            per_page: Optional[int] = None
    ) -> List[EntityResponse]:
        params = {
            'title': title,
            'verified': verified,
            'page': page,
            'perPage': per_page
        }
        logger.info(f'Получение списка сущностей с параметрами: {params}')

        response = self.get(data_api.GET_ALL_ENDPOINT, params=params)
        raw_response = response.json()
        entities_data = raw_response.get('entity', [])      # извлекаем массив из ключа 'entity'
        logger.info(f'Получено {len(entities_data)} сущностей')
        
        # Десериализация списка
        return [EntityResponse.model_validate(item) for item in entities_data]

    @allure.step('Обновление сущности с ID "{entity_id}"')
    def update_entity(self, entity_id: str, entity_data: EntityRequest) -> None:
        logger.info(f'Обновление сущности с ID {entity_id} с данными: {entity_data.model_dump()}')
        self.patch(
            data_api.PATCH_ENDPOINT.format(id=entity_id),
            json=entity_data.model_dump()
        )
        logger.info(f'Сущность с ID {entity_id} обновлена успешно')

    @allure.step('Удаление сущности с ID "{entity_id}"')
    def delete_entity(self, entity_id: str) -> None:
        logger.info(f'Удаление сущности с ID: {entity_id}')
        self.delete(data_api.DELETE_ENDPOINT.format(id=entity_id))
        logger.info(f'Сущность с ID {entity_id} удалена успешно')
