import datetime
import random
import string
from constants import CURRENCY, CURRENCY_SYMBOL


def generate_id(prefix: str = "CMD") -> str:
    """Génère un identifiant unique avec un préfixe donné.
    
    Exemples : CMD-143022-AKZ, EMP-143025-X7P
    """
    timestamp = datetime.datetime.now().strftime("%H%M%S")
    suffix = "".join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"{prefix}-{timestamp}-{suffix}"


def format_currency(amount: float, currency: str = CURRENCY) -> str:
    """Formate un montant avec la devise du restaurant."""
    return f"{amount:,.0f} {currency}"


def format_currency_symbol(amount: float) -> str:
    """Formate avec le symbole local (ex: 12 500 F CFA)"""
    return f"{amount:,.0f} {CURRENCY_SYMBOL}"


def validate_phone(phone: str) -> bool:
    """Vérifie qu'un numéro de téléphone est valide (8 à 12 chiffres)."""
    # Nettoyage du numéro
    digits = ''.join(filter(str.isdigit, phone))
    return 8 <= len(digits) <= 12


def validate_positive_number(value: str | float) -> tuple[bool, float]:
    """
    Vérifie qu'une valeur représente un nombre positif.
    Retourne (valide: bool, valeur: float)
    """
    try:
        number = float(value)
        return number > 0, number
    except (ValueError, TypeError):
        return False, 0.0


def get_current_datetime() -> str:
    """Retourne la date et l'heure actuelles au format français."""
    return datetime.datetime.now().strftime("%d/%m/%Y à %H:%M")


def truncate_text(text: str, max_length: int = 30) -> str:
    """Tronque un texte trop long."""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def print_separator(char: str = "─", width: int = 60) -> None:
    """Affiche une ligne de séparation."""
    print(char * width)


def print_header(title: str, width: int = 60) -> None:
    """Affiche un bel en-tête dans la console."""
    print_separator("═", width)
    print(title.center(width))
    print_separator("═", width)


def print_menu_title() -> None:
    """Affiche le titre du restaurant (utile pour le menu principal)."""
    print_header(RESTAURANT_NAME)
    print(f"{RESTAURANT_ADDRESS.center(60)}")
    print()


# Fonction bonus utile pour ce projet
def clear_screen() -> None:
    """Efface l'écran de la console (multi-plateforme)."""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')