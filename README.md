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

## 🧰 Configuration

### 🔑 Variables d'environnement

Crée un fichier `.env` à la racine :

```env
OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxxxxxx"
```

---

## ✅ Lancer l'application

```bash
streamlit run app.py
```

---

## 📸 Screenshots

### 💡 Vue d'accueil

![Accueil](assets/screenshot_home.png)

### 🥗 Suggestions recettes

![Recettes](assets/screenshot_recipes.png)

### 📷 Scan code-barres

![Scan](assets/screenshot_scan.png)

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

