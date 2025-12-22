from fastapi import APIRouter

from workout_api.atleta.controller import router as atleta
from workout_api.categorias.controller import router as categoria
from workout_api.centro_treinamento.controller import router as centro_treinamento
router = APIRouter()

router.include_router(atleta, prefix="/atleta", tags=["atleta"])
router.include_router(categoria, prefix="/categoria", tags=["categoria"])
router.include_router(centro_treinamento, prefix="/centro_treinamento", tags=["centro_treinamento"])