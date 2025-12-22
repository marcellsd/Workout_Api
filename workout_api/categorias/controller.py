from fastapi import APIRouter
from workout_api.categorias.schemas import CategoriaIn, CategoriaOut
from workout_api.contrib.dependencies import DatabaseDependency
from workout_api.categorias.models import CategoriaModel
from fastapi import Body, HTTPException
from uuid import uuid4
from fastapi import status
from sqlalchemy import select
from typing import List
from pydantic import UUID4

router = APIRouter()

@router.post("/", response_model=CategoriaOut, summary="Cria uma nova categoria", status_code=status.HTTP_201_CREATED)
async def create_categoria(db_session: DatabaseDependency, categoria_in: CategoriaIn = Body(...)):
    categoria_out = CategoriaOut(id=uuid4(), **categoria_in.model_dump())
    categoria_model = CategoriaModel(**categoria_out.model_dump())
    db_session.add(categoria_model)
    await db_session.commit()
    return categoria_out

@router.get("/", response_model=list[CategoriaOut], summary="Lista todas as categorias", status_code=status.HTTP_200_OK)
async def list_categorias(db_session: DatabaseDependency):
    categorias: List[CategoriaOut] = (await db_session.execute(select(CategoriaModel))).scalars().all()
    return categorias

@router.get("/{categoria_id}", response_model=CategoriaOut, summary="Obtém uma categoria por ID", status_code=status.HTTP_200_OK)
async def get_categoria(categoria_id: UUID4, db_session: DatabaseDependency):
    categoria: CategoriaOut | None = (await db_session.execute(select(CategoriaModel).filter_by(id=categoria_id))).scalars().first()
    if not categoria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoria não encontrada")
    return categoria