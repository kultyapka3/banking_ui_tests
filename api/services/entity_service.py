import requests
import allure

from typing import List, Optional

from api.models.entity import EntityRequest, EntityResponse
from data import data_api

class EntityService:
    def __init__(self, base_url=data_api.BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()

    @allure.step('Создание сущности')
    def create_entity(self, entity_data: EntityRequest) -> str:
        response = self.session.post(
            f'{self.base_url}/api/create',
            json=entity_data.model_dump()
        )
        response.raise_for_status()

        return response.text

    @allure.step('Получение сущности с ID "{entity_id}"')
    def get_entity(self, entity_id: str) -> EntityResponse:
        response = self.session.get(f'{self.base_url}/api/get/{entity_id}')
        response.raise_for_status()
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
        params = {}

        if title is not None:
            params['title'] = title
        if verified is not None:
            params['verified'] = verified
        if page is not None:
            params['page'] = page
        if per_page is not None:
            params['perPage'] = per_page

        response = self.session.get(f'{self.base_url}/api/getAll', params=params)
        response.raise_for_status()
        raw_response = response.json()
        entities_data = raw_response.get('entity', [])      # извлекаем массив из ключа 'entity'
        
        # Десериализация списка
        return [EntityResponse.model_validate(item) for item in entities_data]

    @allure.step('Обновление сущности с ID "{entity_id}')
    def update_entity(self, entity_id: str, entity_data: EntityRequest) -> None:
        response = self.session.patch(
            f'{self.base_url}/api/patch/{entity_id}',
            json=entity_data.model_dump()
        )
        response.raise_for_status()

    @allure.step('Удаление сущности с ID "{entity_id}')
    def delete_entity(self, entity_id: str) -> None:
        response = self.session.delete(f'{self.base_url}/api/delete/{entity_id}')
        response.raise_for_status()
