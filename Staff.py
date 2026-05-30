from typing import List, Optional, Union
from models import Staff, Manager
from constants import STAFF_ROLES
from utils import validate_phone
import file_handler


class StaffManager:
    """Manages restaurant staff."""

    def __init__(self) -> None:
        self.__employees: List[Union[Staff, Manager]] = []

    def add_employee(self, employee: Union[Staff, Manager]) -> None:
        """Adds an employee after validation."""
        if employee.role not in STAFF_ROLES:
            raise ValueError(f"Invalid role. Possible roles: {STAFF_ROLES}")
        if employee.phone and not validate_phone(employee.phone):
            raise ValueError(f"Invalid phone number: {employee.phone}")
        if employee.phone and self.get_by_phone(employee.phone):
            raise ValueError(f"Phone {employee.phone} already exists.")
        self.__employees.append(employee)

    def remove_employee(self, name: str) -> bool:
        """Removes an employee by name."""
        for i, emp in enumerate(self.__employees):
            if emp.name.lower() == name.lower():
                self.__employees.pop(i)
                return True
        return False

    def get_by_role(self, role: str) -> List[Staff]:
        """Returns employees by role."""
        return [e for e in self.__employees if e.role == role] if role in STAFF_ROLES else []

    def get_on_shift(self) -> List[Staff]:
        """Returns employees on shift."""
        return [e for e in self.__employees if e.is_on_shift]

    def get_by_phone(self, phone: str) -> Optional[Staff]:
        """Finds an employee by phone."""
        return next((e for e in self.__employees if e.phone == phone), None)

    def display_all_staff(self) -> None:
        """Displays all staff."""
        if not self.__employees:
            print("No employees registered.")
            return
        print("\n" + "═" * 60)
        print("RESTAURANT STAFF".center(60))
        print("═" * 60)
        [print(emp.get_info()) for emp in self.__employees]

    def calculate_total_payroll(self) -> float:
        """Calculates total payroll."""
        return sum(emp.salary for emp in self.__employees)

    def save(self) -> None:
        """Saves staff to CSV."""
        file_handler.save_staff_to_csv(self.__employees)

    def load(self) -> None:
        """Loads staff from CSV."""
        self.__employees = [
            Staff(name=r["Name"], role=r["Role"], salary=float(r["Salary"]),
                  phone=r["Phone"], is_on_shift=r.get("In Shift", "No") == "Yes")
            for r in file_handler.load_staff_from_CSV()
        ]
        print(f"✓ {len(self.__employees)} employees loaded from CSV.")

    def get_all(self) -> List[Staff]:
        """Returns a copy of the employee list."""
        return self.__employees.copy()
