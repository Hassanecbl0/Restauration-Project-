import datetime
import random
import string
from constants import CURRENCY, CURRENCY_SYMBOL,RESTAURANT_ADDRESS,RESTAURANT_NAME


def generate_id(prefix: str = "CMD") -> str:
    """Generate a unique identifier with a given prefix.
    """
    timestamp = datetime.datetime.now().strftime("%H%M%S")
    suffix = "".join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"{prefix}-{timestamp}-{suffix}"


def format_currency(amount: float, currency: str = CURRENCY) -> str:
    """Format the amount using the restaurant's currency."""
    return f"{amount:,.0f} {currency}"


def format_currency_symbol(amount: float) -> str:
    """Format using the local currency symbol."""
    return f"{amount:,.0f} {CURRENCY_SYMBOL}"


def validate_phone(phone: str) -> bool:
    """Check that a phone number is valid."""
    digits = ''.join(filter(str.isdigit, phone))
    return 8 <= len(digits) <= 12


def validate_positive_number(value: str | float) -> tuple[bool, float]:
    """
    Check that a value represents a positive number.
    
    """
    try:
        number = float(value)
        return number > 0, number
    except (ValueError, TypeError):
        return False, 0.0


def get_current_datetime() -> str:
    """Return the current date and time in french format."""
    return datetime.datetime.now().strftime("%d/%m/%Y à %H:%M")


def truncate_text(text: str, max_length: int = 30) -> str:
    """Truncates overly long texts."""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def print_separator(char: str = "─", width: int = 60) -> None:
    """Displays a separator line."""
    print(char * width)


def print_header(title: str, width: int = 60) -> None:
    """Displays a nice header in the console."""
    print_separator("═", width)
    print(title.center(width))
    print_separator("═", width)


def print_menu_title() -> None:
    """Displays the restaurant's title."""
    print_header(RESTAURANT_NAME)
    print(f"{RESTAURANT_ADDRESS.center(60)}")
    print()



def clear_screen() -> None:
    """Clears the screen in the console."""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')
