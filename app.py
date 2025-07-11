from datetime import datetime

import streamlit as st

from utils import (
    add_product,
    get_expiring_products,
    load_data,
    remove_product,
    suggest_multiple_recipes,
    update_product,
)

st.set_page_config(page_title="FiniTonYaourt", page_icon="🥣", layout="wide")

st.title("🥣 FiniTonYaourt")
st.subheader("Ton fidèle assistant anti-gaspi pour le frigo !")

# --- Init états ---
if "edit_product" not in st.session_state:
    st.session_state["edit_product"] = None

if (
    "recipes_suggestions" not in st.session_state
    or st.session_state["recipes_suggestions"] is None
):
    st.session_state["recipes_suggestions"] = []

if "show_add_form" not in st.session_state:
    st.session_state["show_add_form"] = False

# --- 1️⃣ Produits expirés ---
st.header("⚠️ Produits qui expirent bientôt")

expiring = get_expiring_products(days=3)

if expiring:
    for p in expiring:
        st.warning(
            f"⏰ {p['nom']} expire le {p['date_expiration']} ! Vite vite vite ! 💨"
        )

    product_names = [p["nom"] for p in expiring]

    if st.button("💡 Proposer 5 idées de plats avec ces produits"):
        st.session_state["recipes_suggestions"] = suggest_multiple_recipes(
            product_names
        )

    for i, suggestion in enumerate(st.session_state["recipes_suggestions"]):
        st.markdown(f"### 🍽️ {suggestion['title']} — ⏱ {suggestion['time']}")
        if st.button("Plus de détails", key=f"details_{i}"):
            st.session_state["show_details"] = i

    if "show_details" in st.session_state:
        idx = st.session_state["show_details"]
        with st.expander(
            f"📄 Détails pour {st.session_state['recipes_suggestions'][idx]['title']}"
        ):
            st.markdown("### Étapes")
            for step_num, step in enumerate(
                st.session_state["recipes_suggestions"][idx]["steps"], start=1
            ):
                st.markdown(f"{step_num}. {step}")
            if st.button("Fermer", key="close_modal"):
                del st.session_state["show_details"]

else:
    st.success("👌 Aucun produit proche de l'expiration. Bravo chef !")

# --- 2️⃣ Frigo actuel ---
st.header("Mon frigo actuel 🧊")

data = load_data()

if data:
    for p in data:
        col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 1, 1])
        col1.markdown(f"**{p['nom']}**")
        col2.markdown(f"Quantité : {p['quantite']}")
        col3.markdown(f"Expire le {p['date_expiration']}")

        if col4.button("🗑️", key=f"delete_{p['nom']}"):
            remove_product(p["nom"])
            st.success(f"✅ Produit '{p['nom']}' supprimé !")
            st.rerun()

        if col5.button("✏️", key=f"edit_{p['nom']}"):
            st.session_state["edit_product"] = p["nom"]
            st.rerun()

        if st.session_state["edit_product"] == p["nom"]:
            with st.form(f"edit_form_{p['nom']}"):
                new_quantite = st.number_input(
                    "Nouvelle quantité",
                    min_value=1,
                    value=p["quantite"],
                    key=f"qty_{p['nom']}",
                )
                new_date_expiration = st.date_input(
                    "Nouvelle date d'expiration",
                    value=datetime.strptime(p["date_expiration"], "%Y-%m-%d"),
                    key=f"date_{p['nom']}",
                )
                new_notes = st.text_area(
                    "Notes",
                    value=p["notes"] if p["notes"] else "",
                    key=f"notes_{p['nom']}",
                )
                submit_edit = st.form_submit_button("Valider")

                if submit_edit:
                    update_product(
                        nom=p["nom"],
                        new_quantite=new_quantite,
                        new_date_expiration=new_date_expiration.strftime("%Y-%m-%d"),
                        new_notes=new_notes if new_notes.strip() else None,
                    )
                    st.success(f"✅ Produit '{p['nom']}' mis à jour !")
                    st.session_state["edit_product"] = None
                    st.rerun()
else:
    st.info("Ton frigo est vide... pour l'instant ! 😋")

# --- 3️⃣ Bouton Ajouter un produit ---
if st.button("➕ Ajouter un nouveau produit"):
    st.session_state["show_add_form"] = True

if st.session_state["show_add_form"]:
    with st.expander("Ajouter un produit", expanded=True):
        with st.form("add_product_form", clear_on_submit=True):
            nom = st.text_input("Nom du produit")
            quantite = st.number_input("Quantité", min_value=1, value=1)
            date_expiration = st.date_input(
                "Date d'expiration", min_value=datetime.today()
            )
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
                st.session_state["show_add_form"] = False
                st.rerun()

        if st.button("Annuler", key="cancel_add"):
            st.session_state["show_add_form"] = False
