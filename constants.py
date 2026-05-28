from pathlib import Path

# ====================== CONFIGURATION DU RESTAURANT ======================
RESTAURANT_NAME: str = "Chez BIT Restaurant"
RESTAURANT_ADDRESS: str = "Ouagadougou, Burkina Faso"
TAX_RATE: float = 0.18          # TVA 18%
CURRENCY: str = "XOF"
CURRENCY_SYMBOL: str = "F CFA"

# ====================== CHEMINS DES FICHIERS ======================
DATA_DIR = Path("data")
MENU_FILE: Path = DATA_DIR / "menu.json"
ORDERS_FILE: Path = DATA_DIR / "orders.txt"
STAFF_FILE: Path = DATA_DIR / "staff.csv"

# ====================== DONNÉES MÉTIER ======================
ORDER_STATUS: tuple[str, ...] = (
    "en attente", 
    "en préparation", 
    "servie", 
    "payée", 
    "annulée"
)

STAFF_ROLES: tuple[str, ...] = (
    "serveur", 
    "cuisinier", 
    "manager", 
    "caissier"
)

MENU_CATEGORIES: tuple[str, ...] = (
    "entrée", 
    "plat principal", 
    "dessert", 
    "boisson"
)

# ====================== LIMITES & CONTRAINTES ======================
MAX_TABLE_NUMBER: int = 20
MIN_ORDER_AMOUNT: float = 500.0