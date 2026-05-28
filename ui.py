from utils import print_header, print_separator
from constants import RESTAURANT_NAME


def show_main_menu() -> str:
    """Display the main menu and return the user's choice."""
    print_header(f"{RESTAURANT_NAME} - MANAGEMENT SYSTEM")
    options = [
        "1. Menu management",
        "2. Order management",
        "3. Table management",
        "4. Staff management",
        "5. Reports & statistics",
        "0. Quit the program",
    ]
    for option in options:
        print(f"  {option}")
    print_separator()
    return input("Your choice → ").strip()


def show_menu_submenu() -> str:
    """Sous-menu : Gestion du Menu."""
    print_header("MENU MANAGEMENT")
    options = [
        "1. View menu items",
        "2. Add a dish",
        "3. Add a drink",
        "4. Modify item availability",
        "5. Remove an item",
        "0. Return to main menu",
    ]
    for opt in options:
        print(f"  {opt}")
    print_separator()
    return input("Your choice → ").strip()


def show_order_submenu() -> str:
    """Sous-menu : Gestion des Commandes."""
    print_header("ORDER MANAGEMENT")
    options = [
        "1. New order",
        "2. Add an item to an order",
        "3. View active orders",
        "4. Change order status",
        "5. Close and bill an order",
        "0. Return to main menu",
    ]
    for opt in options:
        print(f"  {opt}")
    print_separator()
    return input("Your choice → ").strip()


def show_table_submenu() -> str:
    """Sous-menu : Gestion des Tables."""
    print_header("TABLE MANAGEMENT")
    options = [
        "1. View table status",
        "2. Assign a table to a customer",
        "3. Release a table",
        "0. Return",
    ]
    for opt in options:
        print(f"  {opt}")
    print_separator()
    return input("Your choice → ").strip()


def show_staff_submenu() -> str:
    """Sous-menu : Gestion du Personnel."""
    print_header("STAFF MANAGEMENT")
    options = [
        "1. See all staff members",
        "2. Add an employee",
        "3. View staff on duty",
        "4. Calculate payroll",
        "0. Return",
    ]
    for opt in options:
        print(f"  {opt}")
    print_separator()
    return input("Your choice → ").strip()


def get_user_input(prompt: str, input_type: type = str, error_msg: str = None):
    """
    Demande une saisie avec validation de type.
    """
    while True:
        try:
            value = input(f"{prompt} : ").strip()
            if value == "" and input_type != str:
                print("  ✗ This field cannot be empty.")
                continue
            return input_type(value)
        except ValueError:
            msg = error_msg or f"  ✗ IInvalid input. Please enter a {input_type.__name__}."
            print(msg)


def confirm_action(message: str = "Confirm this action") -> bool:
    """Demande confirmation (o/n)."""
    while True:
        response = input(f"{message} ? (o/n) : ").strip().lower()
        if response in ["o", "oui", "y"]:
            return True
        if response in ["n", "non"]:
            return False
        print("  ✗ Please respond with 'o' or 'n'.")