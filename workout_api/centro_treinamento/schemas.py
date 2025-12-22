from typing import Annotated
from pydantic import Field, UUID4

from workout_api.contrib.schemas import BaseSchema


class CentroTreinamento(BaseSchema):
    nome: Annotated[str, Field(description="Nome do centro de treinamento", examples=["CT 084"], max_length=20)]
    endereco: Annotated[str, Field(description="Endereço do centro de treinamento", examples=["Rua X, Q02"], max_length=60)]
    proprietario: Annotated[str, Field(description="Nome do proprietario", examples=["José"], max_length=30)]

class CentroTreinamentoAtleta(BaseSchema):
    nome: Annotated[str, Field(description="Nome do atleta do centro de treinamento", examples=["CT 084"], max_length=20)]

class CentroTreinamentoIn(CentroTreinamento):
    pass

class CentroTreinamentoOut(CentroTreinamento):
    id: Annotated[UUID4, Field(description="ID do centro de treinamento")]