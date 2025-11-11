import allure

from typing import List, Optional

from api.services.base_api import APIClient
from api.models.entity import EntityRequest, EntityResponse
from data import data_api

class EntityService(APIClient):
    def __init__(self, base_url: str = data_api.BASE_URL):
        super().__init__(base_url)

    @allure.step('Создание сущности')
    def create_entity(self, entity_data: EntityRequest) -> str:
        response = self.post(
            data_api.CREATE_ENDPOINT,
            json=entity_data.model_dump()
        )

        return response.text

    @allure.step('Получение сущности с ID "{entity_id}"')
    def get_entity(self, entity_id: str) -> EntityResponse:
        response = self.get(data_api.GET_ENDPOINT.format(id=entity_id))
        entity_data = response.json()

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

        response = self.get(data_api.GET_ALL_ENDPOINT, params=params)
        raw_response = response.json()
        entities_data = raw_response.get('entity', [])      # извлекаем массив из ключа 'entity'
        
        # Десериализация списка
        return [EntityResponse.model_validate(item) for item in entities_data]

    @allure.step('Обновление сущности с ID "{entity_id}"')
    def update_entity(self, entity_id: str, entity_data: EntityRequest) -> None:
        response = self.patch(
            data_api.PATCH_ENDPOINT.format(id=entity_id),
            json=entity_data.model_dump()
        )

    @allure.step('Удаление сущности с ID "{entity_id}"')
    def delete_entity(self, entity_id: str) -> None:
        response = self.delete(data_api.DELETE_ENDPOINT.format(id=entity_id))
