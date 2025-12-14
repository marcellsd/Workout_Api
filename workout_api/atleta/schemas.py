from typing import Annotated
from pydantic import PositiveFloat, Field

from workout_api.contrib.schemas import BaseSchema


class Atleta(BaseSchema):
    nome: Annotated[str, Field(description="Nome do atleta", examples=["João"],  max_length=50)]
    cpf: Annotated[str, Field(description="CPF do atleta", examples=["123456789000"], min_length=11, max_length=11)]
    idade: Annotated[int, Field(description="Idade do atleta", examples=[25])]
    peso: Annotated[PositiveFloat, Field(description="Peso do atleta (kg)", examples=[75.5])]
    altura: Annotated[PositiveFloat, Field(description="Altura do atleta (m)", examples=[1.7])]
    sexo: Annotated[str, Field(description="Sexo do atleta", examples=["M"],  max_length=1)]