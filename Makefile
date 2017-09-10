.PHONY: train test run-api run-ui

train:
	python ml/training/train.py

test:
	pytest backend/tests

run-api:
	uvicorn app.main:app --app-dir backend --reload --port 8000

run-ui:
	cd frontend && npm install && npm run dev
