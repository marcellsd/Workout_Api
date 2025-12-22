from fastapi import APIRouter
from workout_api.centro_treinamento.schemas import CentroTreinamentoIn, CentroTreinamentoOut
from workout_api.contrib.dependencies import DatabaseDependency
from fastapi import Body, HTTPException
from workout_api.centro_treinamento.models import CentroTreinamentoModel
from uuid import uuid4
from fastapi import status
from sqlalchemy import select
from typing import List
from pydantic import UUID4

router = APIRouter()

@router.post("/", response_model=CentroTreinamentoOut, summary="Cria um novo centro de treinamento", status_code=status.HTTP_201_CREATED)
async def create_centro_treinamento(db_session: DatabaseDependency, centro_treinamento_in: CentroTreinamentoIn = Body(...)) -> CentroTreinamentoOut:
    centro_treinamento_out = CentroTreinamentoOut(id=uuid4(), **centro_treinamento_in.model_dump())
    centro_treinamento_model = CentroTreinamentoModel(**centro_treinamento_out.model_dump())
    db_session.add(centro_treinamento_model)
    await db_session.commit()
    return centro_treinamento_out

@router.get("/", response_model=list[CentroTreinamentoOut], summary="Lista todos os centros de treinamento", status_code=status.HTTP_200_OK)
async def list_centros_treinamento(db_session: DatabaseDependency) -> List[CentroTreinamentoOut]:
    centros_treinamento_out: List[CentroTreinamentoOut] = (await db_session.execute(select(CentroTreinamentoModel))).scalars().all()
    return centros_treinamento_out

@router.get("/{centro_treinamento_id}", response_model=CentroTreinamentoOut, summary="Obtém um centro de treinamento por ID", status_code=status.HTTP_200_OK)
async def get_centro_treinamento(centro_treinamento_id: UUID4, db_session: DatabaseDependency) -> CentroTreinamentoOut:
    centro_treinamento_out: CentroTreinamentoOut | None = await (db_session.execute(select(CentroTreinamentoModel).filter_by(id=centro_treinamento_id))).scalars().first()
    if not centro_treinamento_out:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Centro de treinamento não encontrado")
    return centro_treinamento_out