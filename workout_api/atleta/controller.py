from fastapi import APIRouter, status
from workout_api.atleta.schemas import AtletaIn, AtletaOut, AtletaUpdate
from workout_api.contrib.dependencies import DatabaseDependency
from fastapi import Body
from sqlalchemy import select
from typing import List
from workout_api.atleta.models import AtletaModel
from uuid import uuid4
from datetime import datetime, timezone
from workout_api.categorias.models import CategoriaModel
from workout_api.centro_treinamento.models import CentroTreinamentoModel
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from pydantic import UUID4
router = APIRouter()


@router.post("/", response_model=AtletaOut, summary="Cria um novo atleta", description="Cria um novo atleta",status_code=status.HTTP_201_CREATED)
async def create_atleta(db_session: DatabaseDependency, atleta_in: AtletaIn = Body(...)):
    categoria_model: CategoriaModel | None = (await db_session.execute(select(CategoriaModel).filter_by(nome=atleta_in.categoria.nome))).scalars().first()
    if not categoria_model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoria não encontrada")

    centro_treinamento_model: CentroTreinamentoModel | None = (await db_session.execute(select(CentroTreinamentoModel).filter_by(nome=atleta_in.centro_treinamento.nome))).scalars().first()
    if not centro_treinamento_model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Centro de treinamento não encontrado")

    try:
        atleta_out = AtletaOut(id=uuid4(), created_at=datetime.utcnow(), **atleta_in.model_dump())
        atleta_model = AtletaModel(**atleta_out.model_dump(exclude={"categoria", "centro_treinamento"}))
        atleta_model.categoria_id = categoria_model.pk_id
        atleta_model.centro_treinamento_id = centro_treinamento_model.pk_id
        db_session.add(atleta_model)
        await db_session.commit()
        return atleta_out
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_303_SEE_OTHER, detail="CPF já cadastrado")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ocorreu um erro ao cadastrar o atleta: " + str(e))

@router.get("/", response_model=list[AtletaOut])
async def get_atletas(db_session: DatabaseDependency):
    atletas: List[AtletaOut] = (await db_session.execute(select(AtletaModel))).scalars().all()
    return atletas

@router.get("/{atleta_id}", response_model=AtletaOut, summary="Obtém um atleta por ID", status_code=status.HTTP_200_OK)
async def get_atleta(atleta_id: UUID4, db_session: DatabaseDependency):
    atleta: AtletaOut | None = (await db_session.execute(select(AtletaModel).filter_by(id=atleta_id))).scalars().first()
    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Atleta não encontrado")
    return atleta

@router.patch("/{atleta_id}", response_model=AtletaOut, summary="Atualiza um atleta por ID", status_code=status.HTTP_200_OK)
async def update_atleta(atleta_id: UUID4, db_session: DatabaseDependency, atleta_update: AtletaUpdate = Body(...)) -> AtletaOut:
    atleta_out: AtletaOut | None = (await db_session.execute(select(AtletaModel).filter_by(id=atleta_id))).scalars().first()
    if not atleta_out:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Atleta não encontrado")

    new_atleta = atleta_update.model_dump(exclude_unset=True)
    
    for key, value in new_atleta.items():
        setattr(atleta_out, key, value)
    
    await db_session.commit()
    await db_session.refresh(atleta_out)
    return atleta_out

@router.delete("/{atleta_id}", summary="Deleta um atleta por ID", status_code=status.HTTP_204_NO_CONTENT)
async def delete_atleta(atleta_id: UUID4, db_session: DatabaseDependency) -> None:
    atleta_out: AtletaOut | None = (await db_session.execute(select(AtletaModel).filter_by(id=atleta_id))).scalars().first()
    if not atleta_out:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Atleta não encontrado")
    await db_session.delete(atleta_out)
    await db_session.commit()