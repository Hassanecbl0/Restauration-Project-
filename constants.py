from pathlib import Path

RESTAURANT_NAME: str = "Taste of Africa"
RESTAURANT_ADDRESS: str = "Ouagadougou, Burkina Faso"
TAX_RATE: float = 0.18          # TVA 18%
CURRENCY: str = "XOF"
CURRENCY_SYMBOL: str = "F CFA"

DATA_DIR = Path("data")
MENU_FILE: Path = DATA_DIR / "menu.json"
ORDERS_FILE: Path = DATA_DIR / "orders.json"
STAFF_FILE: Path = DATA_DIR / "staff.csv"

ORDER_STATUS: tuple[str, ...] = (
    "waiting", 
    "in preparation", 
    "served", 
    "paid", 
    "cancelled"
)

STAFF_ROLES: tuple[str, ...] = (
    "server", 
    "chef", 
    "manager", 
    "cashier"
)

MENU_CATEGORIES: tuple[str, ...] = (
    "starter", 
    "main course", 
    "dessert", 
    "drink"
)

MAX_TABLE_NUMBER: int = 20
MIN_ORDER_AMOUNT: float = 500.0
