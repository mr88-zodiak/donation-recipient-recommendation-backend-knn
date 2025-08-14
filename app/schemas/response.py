from pydantic import BaseModel
from pydantic.generics import GenericModel
from typing import Optional, Generic, TypeVar, List

T = TypeVar("T")


class SuksesRespon(BaseModel):
    status_code: int
    message: Optional[str] = None


class SuksesResponGet(GenericModel, Generic[T]):
    status_code: int
    data: List[T]

class SuksesResponId(GenericModel, Generic[T]):
    status_code: int
    data: T


class GagalRespon(BaseModel):
    status_code: int
    message: str
