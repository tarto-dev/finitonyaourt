import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from dotenv import load_dotenv
from openai import OpenAI

DATA_FILE = Path("data/data.json")

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def load_data() -> List[Dict]:
    """Load products from the JSON file."""
    if not DATA_FILE.exists():
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data
    except json.JSONDecodeError:
        return []


def save_data(data: List[Dict]) -> None:
    """Save products to the JSON file."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def add_product(
    nom: str,
    quantite: Optional[int],
    date_expiration: str,
    notes: Optional[str] = None,
) -> None:
    """Add a new product to the list and save."""
    data = load_data()
    product = {
        "nom": nom,
        "quantite": quantite,
        "date_expiration": date_expiration,
        "notes": notes,
        "ajoute_le": datetime.now().strftime("%Y-%m-%d"),
    }
    data.append(product)
    save_data(data)


def get_expiring_products(days: int = 3) -> List[Dict]:
    """Return products expiring within 'days' days."""
    data = load_data()
    today = datetime.today()
    soon = []

    for product in data:
        try:
            exp_date = datetime.strptime(product["date_expiration"], "%Y-%m-%d")
            delta = (exp_date - today).days
            if 0 <= delta <= days:
                soon.append(product)
        except ValueError:
            continue

    return soon


def remove_product(nom: str) -> None:
    """Remove a product by its name."""
    data = load_data()
    new_data = [p for p in data if p["nom"] != nom]
    save_data(new_data)


def update_product(
    nom: str, new_quantite: int, new_date_expiration: str, new_notes: Optional[str]
) -> None:
    """Update an existing product by name."""
    data = load_data()
    for p in data:
        if p["nom"] == nom:
            p["quantite"] = new_quantite
            p["date_expiration"] = new_date_expiration
            p["notes"] = new_notes
            break
    save_data(data)


def suggest_multiple_recipes(products: List[str]) -> List[dict]:
    """
    Get 5 recipe ideas using a list of products.

    Returns a list of dicts with keys: title, time, and steps.
    """
    ingredients = ", ".join(products)
    prompt = (
        f"J'ai ces ingrédients dans mon frigo qui vont bientôt expirer : "
        f"{ingredients}. "
        "Propose-moi 5 idées de plats simples et rapides. "
        "Pour chaque plat, donne absolument ces éléments dans ce format précis :\n\n"
        "Titre: <titre du plat>\n"
        "Temps: <temps de préparation approximatif>\n"
        "Étapes:\n1. Première étape\n2. Deuxième étape\n\n"
        "Sépare chaque recette par la ligne '@@@END@@@'. "
        "Ne donne aucun texte en plus à la fin et respecte strictement ce format."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "Tu es un assistant cuisine créatif et amusant.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )
        content = response.choices[0].message.content
    except Exception as e:
        print("Erreur OpenAI:", e)
        return []

    suggestions = []
    blocks = content.split("@@@END@@@")
    for block in blocks:
        lines = block.strip().split("\n")
        if not lines or lines == [""]:
            continue

        title_line = next((line for line in lines if line.startswith("Titre:")), None)
        title = (
            title_line.replace("Titre:", "").strip() if title_line else "Titre inconnu"
        )

        time_line = next((line for line in lines if line.startswith("Temps:")), None)
        time = (
            time_line.replace("Temps:", "").strip()
            if time_line
            else "Temps non précisé"
        )

        steps_idx = next(
            (i for i, line in enumerate(lines) if line.startswith("1.")), None
        )
        if steps_idx is None:
            continue

        steps = lines[steps_idx:]
        steps_cleaned = []

        steps_idx = next(
            (i for i, line in enumerate(lines) if line.startswith("1.")), None
        )

        if steps_idx is not None:
            steps = lines[steps_idx:]
            for step in steps:
                step_clean = step.lstrip("1234567890. ").strip()
                if not step_clean:
                    continue
                if (
                    "bon appétit" in step_clean.lower()
                    or "j'espère" in step_clean.lower()
                ):
                    continue
                steps_cleaned.append(step_clean)

        # Plus jamais d'erreur : steps_cleaned est toujours défini (même vide)
        if steps_cleaned:
            suggestions.append(
                {
                    "title": title,
                    "time": time,
                    "steps": steps_cleaned,
                }
            )

    if not suggestions:
        suggestions.append(
            {
                "title": title,
                "time": time,
                "steps": steps_cleaned,
            }
        )

    return suggestions
