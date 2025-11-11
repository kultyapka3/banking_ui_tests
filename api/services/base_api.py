import requests
import logging

logger = logging.getLogger(__name__)

class APIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()

    # Базовый метод для отправки запросов
    def _request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        url = f'{self.base_url}{endpoint}'
        logger.info(f'Отправка {method} запроса на {url} с параметрами: {kwargs}')

        response = self.session.request(method, url, **kwargs)
        logger.info(f'Получен ответ {response.status_code} для {method} {url}')

        response.raise_for_status()

        return response

    def get(self, endpoint: str, **kwargs) -> requests.Response:
        logger.debug(f'Вызов GET для "{endpoint}"')

        return self._request('GET', endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs) -> requests.Response:
        logger.debug(f'Вызов POST для "{endpoint}"')

        return self._request('POST', endpoint, **kwargs)

    def patch(self, endpoint: str, **kwargs) -> requests.Response:
        logger.debug(f'Вызов PATCH для "{endpoint}"')

        return self._request('PATCH', endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        logger.debug(f'Вызов DELETE для "{endpoint}"')

        return self._request('DELETE', endpoint, **kwargs)
