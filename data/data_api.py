from typing import Final

# Конфигурации
BASE_URL: Final[str] = 'http://localhost:8080'

# Эндпоинты
CREATE_ENDPOINT: Final[str] = '/api/create'
GET_ENDPOINT: Final[str] = '/api/get/{id}'
GET_ALL_ENDPOINT: Final[str] = '/api/getAll'
PATCH_ENDPOINT: Final[str] = '/api/patch/{id}'
DELETE_ENDPOINT: Final[str] = '/api/delete/{id}'
