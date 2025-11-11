from pydantic import BaseModel

from typing import List, Optional

# Модель для дополнительной информации о сущности в запросе
class AdditionRequest(BaseModel):
    additional_info: Optional[str] = None
    additional_number: Optional[int] = None

# Модель для дополнительной информации о сущности в ответе
class AdditionResponse(BaseModel):
    id: Optional[int] = None
    additional_info: Optional[str] = None
    additional_number: Optional[int] = None

# Модель для отправки сущности (POST, PATCH)
class EntityRequest(BaseModel):
    addition: Optional[AdditionRequest] = None
    important_numbers: List[int] = []
    title: str
    verified: bool

# Модель для получения сущности (GET)
class EntityResponse(BaseModel):
    id: int
    addition: Optional[AdditionResponse] = None
    important_numbers: List[int] = []
    title: str
    verified: bool
