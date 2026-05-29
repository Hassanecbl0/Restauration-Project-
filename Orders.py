import datetime
import json
import os
import sys
from typing import List, Optional, Dict, Any
import pathlib

from models import Order, Table, MenuItem, Customer
from constants import ORDER_STATUS as order_STATUS
from constants import MAX_TABLE_NUMBER, ORDERS_FILE
from utils import generate_id


class OrderManager:
    def __init__(self, table_manager: 'TableManager') -> None:
        self.__active_orders: Dict[str, Order] = {}
        self.__completed_orders: List[Order] = []
        self.__table_manager = table_manager
        self.load()

    def create_order(self, table_number: int, server_name: str) -> Order:
        if not (1 <= table_number <= MAX_TABLE_NUMBER):
            raise ValueError(f"Invalid table number (1-{MAX_TABLE_NUMBER})")
        
        order_id = generate_id("CMD")
        order = Order(order_id, table_number, server_name)
        self.__active_orders[order_id] = order
        return order

    def get_order(self, order_id: str) -> Optional[Order]:
        return self.__active_orders.get(order_id)

    def close_order(self, order_id: str) -> bool:
        order = self.__active_orders.pop(order_id, None)
        if not order:
            return False
            
        paid_status = self._get_paid_status_value()
        old_status = getattr(order, "status", None)
        order.update_status(paid_status)
        
        try:
            self._save_order_to_file(order)
        except Exception as e:
            if old_status is not None:
                order.update_status(old_status)
            self.__active_orders[order_id] = order
            print(f"Error saving command: {e}")
            return False
            
        self.__completed_orders.append(order)
        self.__table_manager.free_table(order.table_number)
        return True

    def _load_orders_from_file(self) -> List[dict]:
        if not os.path.exists(ORDERS_FILE):
            return []
        try:
            with open(ORDERS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except (json.JSONDecodeError, IOError):
            return []

    def _normalize_created_at(self, created_at_value: Any) -> Optional[datetime.datetime]:
        if created_at_value is None:
            return None
        if isinstance(created_at_value, datetime.datetime):
            return created_at_value
        if isinstance(created_at_value, datetime.date):
            return datetime.datetime.combine(created_at_value, datetime.time.min)
        if isinstance(created_at_value, str):
            try:
                return datetime.datetime.fromisoformat(created_at_value)
            except ValueError:
                try:
                    d = datetime.date.fromisoformat(created_at_value)
                    return datetime.datetime.combine(d, datetime.time.min)
                except ValueError:
                    return None
        return None

    def _get_paid_status_value(self) -> str:
        if isinstance(order_STATUS, dict):
            return order_STATUS.get("PAID") or "PAID"
        return "PAID"

    def _is_order_paid(self, order_obj: Optional[Order] = None, order_dict: Optional[dict] = None) -> bool:
        paid_value = self._get_paid_status_value()
        if order_obj is not None:
            status = getattr(order_obj, "status", None)
            if status is not None:
                return str(status).lower() == str(paid_value).lower()
            for attr in ("is_paid", "paid", "payment_status"):
                v = getattr(order_obj, attr, None)
                if v is None:
                    continue
                if isinstance(v, bool):
                    return v
                return str(v).lower() == str(paid_value).lower()
                
        if order_dict is not None:
            for key in ("status", "order_status", "payment_status"):
                if key in order_dict:
                    return str(order_dict.get(key)).lower() == str(paid_value).lower()
            for key in ("is_paid", "paid"):
                if key in order_dict:
                    v = order_dict.get(key)
                    if isinstance(v, bool):
                        return v
                    return str(v).lower() == str(paid_value).lower()
        return False 

    def _save_order_to_file(self, order) -> None:
        existing = self._load_orders_from_file()
        by_id: Dict[str, dict] = {}
        for item in existing:
            if not isinstance(item, dict):
                continue
            oid = item.get("order_id") or item.get("id")
            if oid:
                by_id[str(oid)] = item
                
        order_dict = order.to_dict()
        if "order_id" not in order_dict and hasattr(order, "order_id"):
            order_dict["order_id"] = getattr(order, "order_id")
        if "id" not in order_dict and hasattr(order, "id"):
            order_dict["id"] = getattr(order, "id")
            
        oid = order_dict.get("order_id") or order_dict.get("id")
        if not oid:
            existing.append(order_dict)
            to_write = existing
        else:
            by_id[str(oid)] = order_dict
            to_write = list(by_id.values())
            
        dir_name = os.path.dirname(ORDERS_FILE)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        with open(ORDERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(to_write, f, indent=4, ensure_ascii=False, default=str)

    def get_active_orders_by_table(self, table_number: int) -> List[Order]:
        return [o for o in self.__active_orders.values() if o.table_number == table_number]

    def get_daily_revenue(self, tax_rate: float = 0.18) -> float:
        today = datetime.date.today()
        total = 0.0
        for order in self.__completed_orders:
            created_at = getattr(order, "created_at", None)
            if isinstance(created_at, str):
                created_at = self._normalize_created_at(created_at)
            if created_at is None:
                continue
            if isinstance(created_at, datetime.datetime):
                order_date = created_at.date()
            elif isinstance(created_at, datetime.date):
                order_date = created_at
            else:
                continue
            if order_date == today:
                total += order.get_total(tax_rate)
        return total

    def display_active_orders(self) -> None:
        if not self.__active_orders:
            print("NO ACTIVE COMMANDS")
            return
        print("\n" + "=" * 60)
        print("ACTIVE COMMANDS".center(60))
        print("=" * 60)
        for order in self.__active_orders.values():
            print(order)
            print("-" * 50)

    def load(self) -> None:
        orders_data = self._load_orders_from_file()
        self.__completed_orders.clear()
        self.__active_orders.clear()
        
        for order_dict in orders_data:
            if not isinstance(order_dict, dict):
                continue
            if "created_at" in order_dict:
                normalized = self._normalize_created_at(order_dict["created_at"])
                if normalized is None:
                    print(f"Invalid date for order {order_dict.get('order_id', order_dict.get('id', 'unknown'))}, ignored", file=sys.stderr)
                    continue
                order_dict["created_at"] = normalized
            try:
                order = Order.from_dict(order_dict)
            except Exception as e:
                print(f"Error loading an order: {e}", file=sys.stderr)
                continue
            
            if self._is_order_paid(order_obj=order, order_dict=order_dict):
                self.__completed_orders.append(order)
        
    def get_all_completed_orders(self) -> List[Order]:
        return self.__completed_orders.copy()


class TableManager:
    def __init__(self, num_tables: int = MAX_TABLE_NUMBER) -> None:
        self.__tables: Dict[int, Table] = {
            i: Table(i, capacity=4) for i in range(1, num_tables + 1)
        }

    def get_table(self, table_number: int) -> Optional[Table]:
        return self.__tables.get(table_number)

    def get_free_tables(self) -> List[Table]:
        return [t for t in self.__tables.values() if not t.is_occupied]

    def occupy_table(self, table_number: int, customer: Customer) -> bool:
        table = self.get_table(table_number)
        if table and not table.is_occupied:
            table.seat_customer(customer)
            return True
        return False

    def free_table(self, table_number: int) -> bool:
        table = self.get_table(table_number)
        if table:
            table.free_table()
            return True
        return False

    def display_table_status(self) -> None:
        print("\n--- STATE OF THE TABLES ---")
        for table in sorted(self.__tables.values(), key=lambda t: t.table_number):
            print(table)