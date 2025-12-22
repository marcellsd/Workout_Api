from fastapi import FastAPI
from workout_api.contrib.routers import router

app = FastAPI(title="WorkoutApi")
app.include_router(router)


