import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

DATA_FILE = Path("data/data.json")


def load_data() -> List[Dict]:
    """Load products from the JSON file."""
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


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
