# 🔥 Image Python officielle
FROM python:3.11-slim

# 🛡️ Installer dépendances système (zbar, libmagic, etc.)
RUN apt-get update && apt-get install -y \
    libzbar0 \
    && rm -rf /var/lib/apt/lists/*

# 🌟 Définir le répertoire de travail
WORKDIR /app

# 🗂️ Copier requirements
COPY requirements.txt .

# 📦 Installer dépendances Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 💾 Copier tout le code
COPY . .

# 🌍 Exposer le port par défaut de Streamlit
EXPOSE 8501

# 🏁 Commande pour démarrer
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
