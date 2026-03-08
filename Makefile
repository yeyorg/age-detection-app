.PHONY: install lint format test proto server gateway evaluate

clean:
	cls
	rm -rf app/__pycache__
	rm -rf frontend/__pycache__
	cls
	cls
	@echo "limpiando proyecto..."

install:
	uv sync

frontend:
	@echo "Frontend implementation pending"
	uv run streamlit run src/age_detection_service/frontend/app.py
lint:
	uv run ruff check src tests

format:
	uv run ruff format src tests

test:
	uv run pytest

server:
	@echo "gRPC server implementation pending"

gateway:
	@echo "REST gateway implementation pending"
