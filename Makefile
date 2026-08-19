.PHONY: help install generate-data seed train evaluate test run-backend run-frontend

help:
	@echo "AI Product Recommendation & Customer Intelligence Platform"
	@echo "Available commands:"
	@echo "  make install        Install Python and Node dependencies"
	@echo "  make generate-data  Generate 1,000+ customers & 500+ products demo data"
	@echo "  make seed           Seed database with users, products, orders, reviews"
	@echo "  make train          Train ML models (TF-IDF, SVD, K-Means, NLP)"
	@echo "  make evaluate       Evaluate model benchmarks"
	@echo "  make test           Run full test suite"
	@echo "  make run-backend    Start FastAPI backend (port 8000)"
	@echo "  make run-frontend   Start Vite React frontend (port 5173)"

install:
	pip install -r backend/requirements.txt
	cd frontend && npm install

generate-data:
	python scripts/generate_demo_data.py

seed:
	python scripts/seed_database.py

train:
	python scripts/train_models.py

evaluate:
	python scripts/evaluate_models.py

test:
	python -m pytest backend/tests

run-backend:
	cd backend && uvicorn app.main:app --reload --port 8000

run-frontend:
	cd frontend && npm run dev
