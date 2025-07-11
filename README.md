# 🥣 FiniTonYaourt

**Ton fidèle assistant anti-gaspi pour le frigo !**

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Pre-commit: enabled](https://img.shields.io/badge/pre--commit-enabled-brightgreen)
![Python](https://img.shields.io/badge/python-3.11+-blue)
![Streamlit](https://img.shields.io/badge/Made%20with-Streamlit-ff4b4b)
![Status](https://img.shields.io/badge/status-in%20progress-orange)

---

## 🚀 Description

FiniTonYaourt t'aide à suivre ce qu'il y a dans ton frigo, éviter le gaspillage et te donne des idées de recettes créatives (grâce à GPT !).

✅ Suivi des produits (quantité, date d'expiration, notes)  
✅ Alertes produits expirant bientôt  
✅ Suggestions de recettes à partir des produits  
✅ Ajout rapide avec **scan de code-barres** (via Open Food Facts)  
✅ Modales modernes pour ajouter ou éditer tes produits  
✅ Mode "Consommé" pour marquer ce que tu as mangé  

---

## 💻 Stack technique

* **Python 3.11+**
* **Streamlit** (UI)
* **OpenAI API** (suggestions recettes)
* **Open Food Facts API** (infos code-barres)
* **pyzbar** & **Pillow** (scan image)

---

## ⚙️ Installation

```bash
git clone https://github.com/ton-compte/finitonyaourt.git
cd finitonyaourt
python3 -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate sur Windows
pip install -r requirements.txt
```

---

🔑 Configurer la clé OpenAI

Pour utiliser la génération automatique de suggestions recettes (via GPT), tu dois fournir une clé OpenAI.

Comment obtenir une clé ?

1️⃣ Crée un compte sur OpenAI2️⃣ Gère tes clés API depuis ton tableau de bord (section API keys)3️⃣ Copie la clé générée (elle commence généralement par sk-...)

Comment la configurer dans le projet ?

Crée un fichier .env à la racine du projet :

OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

C’est tout ! Le projet détectera automatiquement la clé et affichera le bouton de suggestions si elle est présente.

---

## ✅ Lancer l'application

```bash
streamlit run app.py
```

---

## 📸 Screenshots

### 💡 Vue d'accueil

![Accueil](https://github.com/user-attachments/assets/3c38430d-e520-4a2e-a880-24f05a327fb3)

### 🥗 Suggestions recettes

![Recettes](https://github.com/user-attachments/assets/7a1163a0-62d8-492d-998e-49c4203d0149)

### 📷 Scan code-barres

![Scan](https://github.com/user-attachments/assets/b4821264-5b3d-4769-802e-49d7eb15b3c4)

---

## 🤝 Contribuer

Les contributions sont les bienvenues !
Propose une idée, corrige un bug ou ajoute un badge "Anti-gaspi Hero" 🌱.

---

## 🫶 Remerciements

* OpenAI pour l'IA
* Open Food Facts pour la base produits
* Tous les yaourts sauvés 💚

---

## 📄 Licence

MIT — fais-en bon usage (et sauve plein de yaourts) !

