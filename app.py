from datetime import datetime

import streamlit as st

from utils import add_product, get_expiring_products, load_data

st.set_page_config(page_title="FiniTonYaourt", page_icon="🥣", layout="wide")

st.title("🥣 FiniTonYaourt")
st.subheader("Ton fidèle assistant anti-gaspi pour le frigo !")

# --- Formulaire d'ajout ---
st.header("Ajouter un produit 🥬")

with st.form("add_product_form", clear_on_submit=True):
    nom = st.text_input("Nom du produit")
    quantite = st.number_input("Quantité", min_value=1, value=1)
    date_expiration = st.date_input("Date d'expiration", min_value=datetime.today())
    notes = st.text_area("Notes (optionnel)", height=80)
    submitted = st.form_submit_button("Ajouter")

    if submitted:
        add_product(
            nom=nom,
            quantite=quantite,
            date_expiration=date_expiration.strftime("%Y-%m-%d"),
            notes=notes if notes.strip() else None,
        )
        st.success(f"✅ Produit '{nom}' ajouté !")

# --- Affichage des produits existants ---
st.header("Mon frigo actuel 🧊")

data = load_data()

if data:
    st.dataframe(data, use_container_width=True)
else:
    st.info("Ton frigo est vide... pour l'instant ! 😋")

# --- Alertes expiration ---
st.header("⚠️ Produits qui expirent bientôt")

expiring = get_expiring_products(days=3)

if expiring:
    for p in expiring:
        st.warning(
            f"⏰ {p['nom']} expire le {p['date_expiration']} ! Vite vite vite ! 💨"
        )
else:
    st.success("👌 Aucun produit proche de l'expiration. Bravo chef !")
