import datetime
from typing import List, Dict, Any
from constants import ORDER_STATUS, MENU_CATEGORIES, MAX_TABLE_NUMBER, STAFF_ROLES, TAX_RATE


# ─────────────────────────────────────────
#  Hiérarchie Person
# ─────────────────────────────────────────

class Person:
    """Classe parent représentant une personne (client ou employé)."""

    def __init__(self, name: str, phone: str) -> None:
        self.__name = name
        self.__phone = phone

    @property
    def name(self) -> str:
        return self.__name

    @property
    def phone(self) -> str:
        return self.__phone

    @phone.setter
    def phone(self, value: str) -> None:
        if len(value) >= 8:
            self.__phone = value
        else:
            raise ValueError("Le numéro de téléphone doit contenir au moins 8 caractères.")

    def get_info(self) -> str:
        return f"Personne: {self.name} | Tél: {self.phone}"

    def __str__(self) -> str:
        return self.get_info()


class Customer(Person):
    """Client du restaurant."""

    def __init__(self, name: str, phone: str, table_number: int) -> None:
        super().__init__(name, phone)
        if not 1 <= table_number <= MAX_TABLE_NUMBER:
            raise ValueError(f"Le numéro de table doit être entre 1 et {MAX_TABLE_NUMBER}")
        self.table_number: int = table_number
        self.order_history: List[str] = []

    def add_to_history(self, order_id: str) -> None:
        self.order_history.append(order_id)

    def get_info(self) -> str:
        return (f"Client: {self.name} | Tél: {self.phone} "
                f"| Table: {self.table_number} | Commandes: {len(self.order_history)}")


class Staff(Person):
    """Employé du restaurant."""

    def __init__(self, name: str, phone: str, role: str, salary: float) -> None:
        super().__init__(name, phone)
        if role not in STAFF_ROLES:
            raise ValueError(f"Rôle invalide. Choix possibles : {STAFF_ROLES}")
        self.__role = role
        self.__salary = salary
        self.is_on_shift: bool = False

    @property
    def role(self) -> str:
        return self.__role

    @property
    def salary(self) -> float:
        return self.__salary

    def clock_in(self) -> None:
        self.is_on_shift = True

    def clock_out(self) -> None:
        self.is_on_shift = False

    def get_info(self) -> str:
        status = "en service" if self.is_on_shift else "hors service"
        return (f"Employé: {self.name} | Rôle: {self.role} "
                f"| Salaire: {self.salary:,.0f} XOF | Statut: {status}")


class Manager(Staff):
    """Manager du restaurant."""

    def __init__(self, name: str, phone: str, salary: float, department: str) -> None:
        super().__init__(name, phone, "manager", salary)
        self.department: str = department
        self.__staff_list: List[Staff] = []

    def add_staff(self, employee: Staff) -> None:
        self.__staff_list.append(employee)

    def get_team_size(self) -> int:
        return len(self.__staff_list)

    def get_info(self) -> str:
        base = super().get_info()
        return f"{base} | Département: {self.department} | Équipe: {self.get_team_size()}"


# ─────────────────────────────────────────
#  Hiérarchie MenuItem
# ─────────────────────────────────────────

class MenuItem:
    """Élément du menu."""

    def __init__(self, item_id: str, name: str, price: float, category: str) -> None:
        self.__item_id = item_id
        self.__name = name
        self.__price = price
        if category not in MENU_CATEGORIES:
            raise ValueError(f"Catégorie invalide. Choix possibles : {MENU_CATEGORIES}")
        self.category = category
        self.available: bool = True

    @property
    def item_id(self) -> str:
        return self.__item_id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def price(self) -> float:
        return self.__price

    @price.setter
    def price(self, value: float) -> None:
        if value > 0:
            self.__price = value
        else:
            raise ValueError("Le prix doit être positif.")

    def display(self) -> str:
        status = "✓" if self.available else "✗"
        return f"[{status}] {self.name} — {self.price:,.0f} XOF ({self.category})"

    def to_dict(self) -> dict:
        return {
            "id": self.item_id,
            "name": self.name,
            "price": self.price,
            "category": self.category,
            "available": self.available,
        }

    def __str__(self) -> str:
        return self.display()


class Dish(MenuItem):
    def __init__(self, item_id: str, name: str, price: float,
                 category: str, ingredients: List[str], prep_time: int) -> None:
        super().__init__(item_id, name, price, category)
        self.ingredients: List[str] = ingredients
        self.prep_time: int = prep_time

    def display(self) -> str:
        base = super().display()
        ingr = ", ".join(self.ingredients[:5])
        return f"{base} | Préparation: {self.prep_time} min | Ingrédients: {ingr}"


class Drink(MenuItem):
    def __init__(self, item_id: str, name: str, price: float,
                 volume_ml: int, alcoholic: bool) -> None:
        super().__init__(item_id, name, price, "boisson")
        self.volume_ml: int = volume_ml
        self.alcoholic: bool = alcoholic

    def display(self) -> str:
        base = super().display()
        alc = "alcoolisée" if self.alcoholic else "sans alcool"
        return f"{base} | {self.volume_ml} ml | {alc}"


# ─────────────────────────────────────────
#  Order & Table
# ─────────────────────────────────────────

class Order:
    """Commande passée par un client."""

    def __init__(self, order_id: str, table_number: int, server_name: str) -> None:
        self.__order_id = order_id
        self.table_number: int = table_number
        self.server_name: str = server_name
        self.items: List[Dict[str, Any]] = []
        self.status: str = ORDER_STATUS[0]
        self.timestamp: str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        self.notes: Dict[str, str] = {}

    @property
    def order_id(self) -> str:
        return self.__order_id

    def add_item(self, item: MenuItem, quantity: int = 1) -> None:
        if quantity < 1:
            raise ValueError("La quantité doit être positive.")
        self.items.append({"item": item, "quantity": quantity})

    def remove_item(self, item_name: str) -> bool:
        for i, entry in enumerate(self.items):
            if entry["item"].name == item_name:
                self.items.pop(i)
                return True
        return False

    def get_subtotal(self) -> float:
        return sum(e["item"].price * e["quantity"] for e in self.items)

    def get_total(self, tax_rate: float = TAX_RATE) -> float:
        return self.get_subtotal() * (1 + tax_rate)

    def update_status(self, new_status: str) -> None:
        if new_status in ORDER_STATUS:
            self.status = new_status
        else:
            raise ValueError(f"Statut invalide. Choix possibles : {ORDER_STATUS}")

    def add_note(self, item_name: str, note: str) -> None:
        self.notes[item_name] = note

    def __str__(self) -> str:
        lines = [f"Commande #{self.order_id} | Table {self.table_number} "
                 f"| {self.timestamp} | Statut: {self.status}"]
        for entry in self.items:
            item = entry["item"]
            lines.append(f"  - {item.name} x{entry['quantity']} = "
                         f"{item.price * entry['quantity']:,.0f} XOF")
        return "\n".join(lines)


class Table:
    """Table du restaurant."""

    def __init__(self, table_number: int, capacity: int) -> None:
        self.table_number: int = table_number
        self.capacity: int = capacity
        self.is_occupied: bool = False
        self.current_customer: Customer | None = None

    def seat_customer(self, customer: Customer) -> None:
        self.is_occupied = True
        self.current_customer = customer

    def free_table(self) -> None:
        self.is_occupied = False
        self.current_customer = None

    def __str__(self) -> str:
        status = "occupée" if self.is_occupied else "libre"
        return f"Table {self.table_number} ({self.capacity} places) — {status}"