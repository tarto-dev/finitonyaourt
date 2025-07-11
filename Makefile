# 🥣 Makefile — FiniTonYaourt

# Active l'environnement virtuel (optionnel)
VENV_ACTIVATE = source venv/bin/activate

# 📜 Help
help:
	@echo ""
	@echo "🍓 FiniTonYaourt — Available commands:"
	@echo ""
	@echo "  make install       → Install dependencies from requirements.txt"
	@echo "  make format        → Format code (black, reorder-imports, isort)"
	@echo "  make lint          → Run linters (flake8, mypy)"
	@echo "  make test          → Run tests with pytest"
	@echo "  make run           → Launch Streamlit app"
	@echo "  make precommit     → Run pre-commit hooks on all files"
	@echo "  make check         → Combo: format + lint + precommit"
	@echo "  make help          → Show this help message"
	@echo ""

# 📦 Install dependencies
install:
	pip install -r requirements.txt

# 🧹 Format code
format:
	black .
	reorder-python-imports --exit-zero-even-if-changed -r .
	isort .

# ✅ Lint code
lint:
	flake8 .
	mypy .

# 🧪 Run tests
test:
	pytest --cov

# 💬 Run Streamlit app
run:
	streamlit run app.py

# ⚡ Run pre-commit hooks
precommit:
	pre-commit run --all-files

# 🔥 Combo
check:
	make format
	make lint
	make precommit

