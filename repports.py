import datetime
from constants import TAX_RATE, CURRENCY, RESTAURANT_NAME, RESTAURANT_ADDRESS
from utils import format_currency, print_header, print_separator


def generate_daily_report(order_manager, staff_manager, menu_manager) -> str:
    """Generates a complete daily report."""
    today = datetime.datetime.now().strftime("%d/%m/%Y")
    revenue = order_manager.get_daily_revenue(TAX_RATE)
    on_shift = len(staff_manager.get_on_shift())
    total_items = len(menu_manager.get_all_items())
    available_items = len(menu_manager.get_available_items())

    lines = [
        "=" * 60,
        f"DAILY REPORT — {RESTAURANT_NAME}".center(60),
        f"Date : {today}".center(60),
        "=" * 60,
        "",
        f"  Revenue of the day : {format_currency(revenue)}",
        f"  Employees on shift : {on_shift}",
        f"  Menu items         : {total_items} ({available_items} available)",
        "",
        "=" * 60,
    ]
    return "\n".join(lines)


def print_receipt(order, tax_rate: float = TAX_RATE) -> None:
    """Prints the detailed receipt of an order."""
    print_header(f"RECEIPT — Order #{order.order_id}")
    print(f"  Table  : {order.table_number}")
    print(f"  Server : {order.server_name}")
    print(f"  Date   : {order.timestamp}")
    print(f"  Status : {order.status.upper()}")
    print_separator()

    for entry in order.items:
        item = entry["item"]
        qty = entry["quantity"]
        subtotal = item.price * qty
        print(f"  {item.name:<28} x{qty:2d}   {format_currency(subtotal):>12}")

    print_separator()

    subtotal = order.get_subtotal()
    taxes = subtotal * tax_rate
    total = order.get_total(tax_rate)

    print(f"  {'Subtotal':<30} {format_currency(subtotal):>12}")
    print(f"  {f'VAT ({tax_rate*100:.0f}%)':<30} {format_currency(taxes):>12}")
    print_separator("─")
    print(f"  {'TOTAL':<30} {format_currency(total):>12}")
    print_separator("═")

    print("  Thank you for your visit !".center(50))
    print(f"  {RESTAURANT_ADDRESS}".center(50))
    print_separator("═")


def print_simple_receipt(order) -> None:
    """Simplified version of the receipt for quick printing."""
    print(f"\n--- Receipt #{order.order_id} ---")
    print(f"Table {order.table_number} | {order.timestamp}")
    print("─" * 40)
    for entry in order.items:
        item = entry["item"]
        print(f"{item.name} x{entry['quantity']} = {format_currency(item.price * entry['quantity'])}")
    print("─" * 40)
    print(f"TOTAL : {format_currency(order.get_total())}")
    print("Thank you !")
    