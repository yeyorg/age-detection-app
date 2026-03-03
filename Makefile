.PHONY: install lint format test proto server gateway evaluate

install:
	uv sync

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
