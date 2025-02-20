from pydantic import BaseModel
from typing import Optional, TypeVar, Generic

T = TypeVar('T')

class CommonResponse(BaseModel, Generic[T]):
    status: int
    message: str
    data: Optional[T] = None
