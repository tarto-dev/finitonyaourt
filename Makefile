.PHONY: help venv install fmt lint type-check docker-build docker-up docker-down docker-logs

help:
	@echo ""
	@echo "📄 Commandes disponibles :"
	@echo "  make venv          → Créer et activer l'environnement virtuel"
	@echo "  make install       → Installer les dépendances Python"
	@echo "  make fmt           → Formatter le code (black, isort)"
	@echo "  make lint          → Lint du code (flake8)"
	@echo "  make type-check    → Vérifier les types (mypy)"
	@echo "  make docker-build  → Builder l'image Docker"
	@echo "  make docker-up     → Lancer l'application (docker-compose)"
	@echo "  make docker-down   → Stopper l'application"
	@echo "  make docker-logs   → Voir les logs"
	@echo ""

venv:
	python3 -m venv venv
	@echo "✅ Venv créé. Active-le avec 'source venv/bin/activate'"

install:
	pip install -r requirements.txt
	@echo "✅ Dépendances installées."

fmt:
	black .
	isort .

lint:
	flake8 .

type-check:
	mypy .

docker-build:
	docker-compose build
	@echo "✅ Image Docker buildée."

docker-up:
	docker-compose up

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f
