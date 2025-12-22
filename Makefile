run:
	@uvicorn workout_api.main:app --reload
create-migrations:
	@PYTHONPATH=$PYTHONPATH:$(pwd) uv run alembic revision --autogenerate -m $(d)
run-migrations:
	@PYTHONPATH=$PYTHONPATH:$(pwd) uv run alembic upgrade head