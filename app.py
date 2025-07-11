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


@st.dialog("Ajouter un produit")
def add_product_dialog():
    nom = st.text_input("Nom du produit")
    quantite = st.number_input("Quantité", min_value=1, value=1)
    date_expiration = st.date_input("Date d'expiration", min_value=datetime.today())
    notes = st.text_area("Notes (optionnel)", height=80)

    col_submit, col_cancel = st.columns(2)

    with col_submit:
        if st.button("Ajouter"):
            add_product(
                nom=nom,
                quantite=quantite,
                date_expiration=date_expiration.strftime("%Y-%m-%d"),
                notes=notes if notes.strip() else None,
            )
            st.success(f"✅ Produit '{nom}' ajouté !")
            st.session_state["show_add_form"] = False
            st.rerun()

    with col_cancel:
        if st.button("Annuler"):
            st.session_state["show_add_form"] = False
            st.rerun()


@st.dialog("Éditer un produit")
def edit_product_dialog(product):
    new_nom = st.text_input("Nom du produit", value=product["nom"])
    new_quantite = st.number_input(
        "Nouvelle quantité", min_value=1, value=product["quantite"]
    )
    new_date_expiration = st.date_input(
        "Nouvelle date d'expiration",
        value=datetime.strptime(product["date_expiration"], "%Y-%m-%d"),
    )
    new_notes = st.text_area(
        "Notes", value=product["notes"] if product["notes"] else ""
    )

    col_submit, col_cancel = st.columns(2)

    with col_submit:
        if st.button("Valider"):
            update_product(
                nom=product["nom"],  # Nom initial pour retrouver l'item
                new_quantite=new_quantite,
                new_date_expiration=new_date_expiration.strftime("%Y-%m-%d"),
                new_notes=new_notes if new_notes.strip() else None,
                new_nom=new_nom,
            )
            st.success(f"✅ Produit '{new_nom}' mis à jour !")
            st.session_state["edit_product"] = None
            st.rerun()

    with col_cancel:
        if st.button("Annuler"):
            st.session_state["edit_product"] = None
            st.rerun()


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
        col1, col2, col3, col4, col5, col6 = st.columns([3, 2, 2, 1, 1, 1])

        col1.markdown(f"**{p['nom']}**")
        col2.markdown(f"Quantité : {p['quantite']}")
        col3.markdown(f"Expire le {p['date_expiration']}")

        if col4.button("🗑️", key=f"delete_{p['nom']}"):
            remove_product(p["nom"])
            st.success(f"✅ Produit '{p['nom']}' supprimé !")
            st.rerun()

        if col5.button("✏️", key=f"edit_{p['nom']}"):
            edit_product_dialog(p)

        if col6.button("✅", key=f"consume_{p['nom']}"):
            remove_product(p["nom"])
            st.success(f"😋 Produit '{p['nom']}' marqué comme consommé !")
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
if "show_add_form" not in st.session_state:
    st.session_state["show_add_form"] = False

# Si la modale n'est pas ouverte, on affiche le bouton
if not st.session_state["show_add_form"]:
    if st.button("➕ Ajouter un nouveau produit"):
        add_product_dialog()

# Si la modale est ouverte
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
            st.rerun()
