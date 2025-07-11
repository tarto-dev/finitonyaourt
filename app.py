from datetime import datetime

import streamlit as st

from utils import (
    add_product,
    get_expiring_products,
    get_product_from_barcode,
    load_data,
    read_barcode,
    remove_product,
    suggest_multiple_recipes,
    update_product,
)

# --- Init states ---
if "edit_product" not in st.session_state:
    st.session_state["edit_product"] = None

if (
    "recipes_suggestions" not in st.session_state
    or st.session_state["recipes_suggestions"] is None
):
    st.session_state["recipes_suggestions"] = []

if "auto_filled_name" not in st.session_state:
    st.session_state["auto_filled_name"] = ""


# --- Modales ---
# --- Modale d'édition ---
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
                nom=product["nom"],
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


# --- Modale d'ajout ---
@st.dialog("Ajouter un produit")
def add_product_dialog():
    st.write("📷 Tu peux scanner un code-barres pour pré-remplir le nom.")

    uploaded_image = st.file_uploader(
        "Importer une photo du code-barres", type=["png", "jpg", "jpeg"]
    )
    if uploaded_image:
        barcode = read_barcode(uploaded_image)
        if barcode:
            product_name = get_product_from_barcode(barcode)
            st.session_state["auto_filled_name"] = product_name
            st.success(f"✅ Produit détecté : {product_name}")
        else:
            st.warning("❌ Aucun code-barres détecté dans l'image.")

    nom_default = st.session_state.get("auto_filled_name", "")
    nom = st.text_input("Nom du produit", value=nom_default)
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
            st.session_state["auto_filled_name"] = ""
            st.rerun()

    with col_cancel:
        if st.button("Annuler"):
            st.session_state["auto_filled_name"] = ""
            st.rerun()


st.set_page_config(page_title="FiniTonYaourt", page_icon="🥣", layout="wide")
st.title("🥣 FiniTonYaourt")
st.subheader("Ton fidèle assistant anti-gaspi pour le frigo !")

# --- Produits expirés ---
st.header("⚠️ Produits qui expirent bientôt")
expiring = get_expiring_products(days=3)

if expiring:
    for p in expiring:
        st.warning(
            f"⏰ {p['nom']} expire le {p['date_expiration']} ! Vite vite vite 💨"
        )

    # --- Suggestions recettes GPT ---
    if st.button("💡 Proposer 5 idées de plats avec ces produits"):
        product_names = [p["nom"] for p in expiring]
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

# --- Frigo actuel ---
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
else:
    st.info("Ton frigo est vide... pour l'instant ! 😋")


# --- Bouton principal pour ouvrir la modale d'ajout ---
if st.button("➕ Ajouter un nouveau produit"):
    add_product_dialog()
