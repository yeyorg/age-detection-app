.PHONY: clean clean-win clean-linux install frontend lint format test server experiment mlflow-ui register validate evaluate

# Windows cleanup
clean-win:
	@echo "Limpiando proyecto (Windows)..."
	@if exist src\age_detection_service\__pycache__ rmdir /s /q src\age_detection_service\__pycache__
	@if exist src\age_detection_service\backend\__pycache__ rmdir /s /q src\age_detection_service\backend\__pycache__
	@if exist src\age_detection_service\frontend\__pycache__ rmdir /s /q src\age_detection_service\frontend\__pycache__
	@if exist tests\__pycache__ rmdir /s /q tests\__pycache__
	@if exist .pytest_cache rmdir /s /q .pytest_cache
	@if exist build rmdir /s /q build
	@if exist dist rmdir /s /q dist
	@for /r %%i in (*.pyc) do @if exist "%%i" del /q "%%i"
	@for /d /r %%i in (__pycache__) do @if exist "%%i" rmdir /s /q "%%i"
	@echo "Proyecto limpio!"

# Linux/Unix cleanup
clean-linux:
	@echo "Limpiando proyecto (Linux/Unix)..."
	rm -rf src/age_detection_service/__pycache__
	rm -rf src/age_detection_service/backend/__pycache__
	rm -rf src/age_detection_service/frontend/__pycache__
	rm -rf tests/__pycache__
	rm -rf .pytest_cache
	rm -rf build dist *.egg-info
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type d -name "__pycache__" -delete 2>/dev/null || true
	@echo "Proyecto limpio!"

# Alias: use clean-win by default (for Windows development)
clean: clean-win

install:
	uv sync

frontend:
	@echo "Frontend implementation"
	uv run streamlit run src/age_detection_service/frontend/app.py

lint:
	uv run ruff check .

format:
	uv run ruff format .

quality: format lint
	@echo "Código limpio y verificado"

test:
	uv run pytest

register:
	uv run python scripts/register_model.py

validate:
	uv run python scripts/validate_model.py

evaluate:
	uv run python scripts/evaluate_model.py

mlflow-ui:
	uv run mlflow ui --port 5000

server:
	uv run uvicorn age_detection_service.backend.api:app --host 0.0.0.0 --port 8000
