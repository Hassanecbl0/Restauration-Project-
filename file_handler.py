import json
import csv
from pathlib import Path
from typing import List, Any
import datetime

from constants import MENU_FILE, ORDERS_FILE, STAFF_FILE
def ensure_data_folder():
    Path("data").mkdir(parents=True, exist_ok=True)

def save_menu_to_json(menu_items: List[Any], filepath: Path = MENU_FILE):
    ensure_data_folder()
    try:
        data = [item.to_dict() for item in menu_items]
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"✅ Menu saved ({len(menu_items)} articles)")
    except Exception as e:
        print(f"❌ Menu save error : {e}")

def load_menu_from_json(filepath: Path = MENU_FILE) -> List[dict]:
    if not filepath.exists():
        return []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading menu from JSON: {e}")
        return []

def append_order_to_file(order_str: str, filepath: Path = ORDERS_FILE):
    ensure_data_folder()
    try:
        with open(filepath, "a", encoding="utf-8") as f:
            f.write(f"=== Command- {datetime.datetime.now():%d/%m/%Y %H:%M} ===\n")
            f.write(order_str + "\n" + "─" * 60 + "\n\n")
        print("✅ Command saved")
    except Exception as e:
        print(f"❌ Error: {e}")

def read_all_orders(filepath: Path = ORDERS_FILE) -> str:
    return filepath.read_text(encoding="utf-8")  if filepath.exists() else "No orders recorded."

def save_staff_to_csv(staff_list: List[Any], filepath: Path = STAFF_FILE):
    ensure_data_folder()
    try:
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Name", "Phone", "Role", "Salary", "In Shift"])
            for emp in staff_list:
                writer.writerow([emp.name, emp.phone, emp.role, f"{emp.salary:.0f}","Yes" if getattr(emp, 'is_on_shift', False) else "No"
                ])
        print(f"✅ Staff saved ({len(staff_list)} employees)")
    except Exception as e:
        print(f"❌ Staff save error: {e}")

def load_staff_from_csv(filepath: Path = STAFF_FILE) -> List[dict]:
    if not filepath.exists():
        return []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return list(csv.DictReader(f))
    except Exception:
        print(f"✗ Error loading staff from CSV: {e}")
        return []