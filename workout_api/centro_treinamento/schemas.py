from typing import Annotated

from pydantic import Field

from workout_api.contrib.schemas import BaseSchema


class CentroTreinamento(BaseSchema):
    nome = Annotated[str, Field(description="Nome do centro de treinamento",examples=["CT 084"], max_length=20)]
    endereco = Annotated[str, Field(description="Endereço do centro de treinamento", examples=["Rua X, Q02"], max_length=60)]
    proprietario = Annotated[str, Field(description="Nome do proprietario", examples=["José"], max_length=30)]
