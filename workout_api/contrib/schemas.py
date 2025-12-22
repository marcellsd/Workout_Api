from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Annotated

class BaseSchema(BaseModel):
    class Config:
        extra = 'forbid'
        from_attributes = True

class OutMixin(BaseModel):
    id: Annotated[UUID, Field(description="ID do registro")]
    created_at: Annotated[datetime, Field(description="Data de criação do registro")]