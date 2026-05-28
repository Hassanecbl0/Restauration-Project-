import sys

from constants import (MENU_FILE, ORDERS_FILE, STAFF_FILE, 
                       TAX_RATE, RESTAURANT_NAME)

from models import Dish, Drink, Staff, Manager, Customer
from menu import MenuManager
from Orders import OrderManager, TableManager
from staff import StaffManager
from reports import generate_daily_report, print_receipt
from ui import (show_main_menu, show_menu_submenu, show_order_submenu,
                show_table_submenu, show_staff_submenu,
                get_user_input, confirm_action)
from utils import generate_id, print_header


def seed_initial_data(menu_mgr: MenuManager, staff_mgr: StaffManager) -> None:
    # Menu
    menu_mgr.add_item(Dish("D001", "Rice with peanut sauce", 2500, "main course",
                           ["rice", "peanut sauce", "chicken"], 25))
    menu_mgr.add_item(Dish("D002", "Grilled tofu", 3000, "main course",
                           ["tofu", "meat"], 30))
    menu_mgr.add_item(Dish("D003", "Vegetable salad", 1200, "starter",
                           ["lettuce", "tomato"], 10))
    menu_mgr.add_item(Drink("B001", "Mineral water", 500, 500, False))
    menu_mgr.add_item(Drink("B002", "Bissap juice", 800, 330, False))
    menu_mgr.add_item(Drink("B003", "Flag Beer", 1200, 600, True))

    # Personnel
    manager = Manager("Amadou Ouédraogo", "+22670000001", 250000, "operations")
    serveur = Staff("Fatima Sawadogo", "+22675000002", "server", 85000)
    cuisinier = Staff("Ibrahim Kaboré", "+22678000003", "chef", 110000)

    manager.clock_in()
    serveur.clock_in()
    cuisinier.clock_in()

    staff_mgr.add_employee(manager)
    staff_mgr.add_employee(serveur)
    staff_mgr.add_employee(cuisinier)


def handle_menu_management(menu_mgr: MenuManager) -> None:
    """Manage the menu."""
    while True:
        choice = show_menu_submenu()
        if choice == "1":
            menu_mgr.display_full_menu()
        elif choice == "2":
            item_id = generate_id("D")
            name = get_user_input("Name of dish")
            price = get_user_input("Price (XOF)", float)
            ingredients_str = get_user_input("Ingredients (separated by comma)")
            prep_time = get_user_input("Preparation time (min)", int)

            ingredients = [i.strip() for i in ingredients_str.split(",")]
            dish = Dish(item_id, name, price, "Main menu", ingredients, prep_time)
            menu_mgr.add_item(dish)
            print(f"✓ '{name}' added to the menu.")
        elif choice == "0":
            break
        else:
            print("  ✗ Invalid option.")


def handle_order_management(order_mgr: OrderManager, menu_mgr: MenuManager) -> None:
    """Manage the orders submenu."""
    current_order = None
    while True:
        choice = show_order_submenu()
        if choice == "1":
            table_num = get_user_input("Number of table", int)
            server = get_user_input("Name of server")
            current_order = order_mgr.create_order(table_num, server)
            print(f"✓ Order {current_order.order_id} created.")

        elif choice == "2":
            if not current_order:
                print("✗ Create an order first.")
                continue
            menu_mgr.display_full_menu()
            item_id = get_user_input("ID of the item")
            item = menu_mgr.get_item_by_id(item_id)
            if item:
                qty = get_user_input("Quantity", int)
                current_order.add_item(item, qty)
                print(f"✓ {qty}x {item.name} added.")
            else:
                print("✗ Item not found.")

        elif choice == "3":
            order_mgr.display_active_orders()
        elif choice == "5":
            if current_order:
                print_receipt(current_order)
                if confirm_action("Confirm closing this order"):
                    order_mgr.close_order(current_order.order_id)
                    print("✓ Order closed.")
                    current_order = None
        elif choice == "0":
            break


def handle_table_management(table_mgr: TableManager) -> None:
    """Manage the tables submenu."""
    while True:
        choice = show_table_submenu()
        if choice == "1":
            table_mgr.display_table_status()
        elif choice == "2": 
            table_num = get_user_input("Number of table", int)
            customer_name = get_user_input("Customer name")
            phone = get_user_input("Phone number")
            customer = Customer(customer_name, phone, table_num)
            if table_mgr.occupy_table(table_num, customer):
                print(f"✓ Table {table_num} attributed to {customer_name}.")
            else:
                print("✗ Cannot attribute this table (already occupied or not found).")
        elif choice == "3":  # Libérer une table
            table_num = get_user_input("Number of table to free", int)
            if table_mgr.free_table(table_num):
                print(f"✓ Table {table_num} freed.")
            else:
                print("✗ Table not found.")
        elif choice == "0":
            break
        else:
            print("  ✗ Invalid option.")


def handle_staff_management(staff_mgr: StaffManager) -> None:
    """Manage the staff submenu."""
    while True:
        choice = show_staff_submenu()
        if choice == "1":
            staff_mgr.display_all_staff()
        elif choice == "2":
            name = get_user_input("Full name")
            phone = get_user_input("Phone number")
            role = get_user_input("Role (server/chef/manager/cashier)")
            salary = get_user_input("Salary (XOF)", float)

            employee = Staff(name, phone, role, salary)
            staff_mgr.add_employee(employee)
            print(f"✓ {name} added as {role}.")
        elif choice == "3":
            on_shift = staff_mgr.get_on_shift()
            print(f"\nEmployees on shift : {len(on_shift)}")
            for emp in on_shift:
                print(emp.get_info())
        elif choice == "4":
            total = staff_mgr.calculate_total_payroll()
            print(f"Total payroll : {total:,.0f} XOF")
        elif choice == "0":
            break
        else:
            print("  ✗ Invalid option.")


def main() -> None:
    """Main function."""
    menu_mgr = MenuManager()
    order_mgr = OrderManager()
    staff_mgr = StaffManager()
    table_mgr = TableManager(num_tables=15)

    seed_initial_data(menu_mgr, staff_mgr)
    menu_mgr.save()

    print_header(f"Welcome to {RESTAURANT_NAME}")
    print("System initialized successfully.\n")

    while True:
        choice = show_main_menu()

        if choice == "1":
            handle_menu_management(menu_mgr)
        elif choice == "2":
            handle_order_management(order_mgr, menu_mgr)
        elif choice == "3":
            handle_table_management(table_mgr)
        elif choice == "4":
            handle_staff_management(staff_mgr)
        elif choice == "5":
            report = generate_daily_report(order_mgr, staff_mgr, menu_mgr)
            print(report)
        elif choice == "0":
            if confirm_action("Quit the application"):
                menu_mgr.save()
                staff_mgr.save()
                print("\nGood bye !")
                sys.exit(0)
        else:
            print("✗ Invalid option.")


if __name__ == "__main__":
    main()