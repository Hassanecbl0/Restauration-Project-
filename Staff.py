from typing import List, Optional, Union
from models import Staff, Manager
from constants import STAFF_ROLES
from utils import validate_phone
import file_handler


class StaffManager:

   def __init__(self):
       self.employees: List[Union[Staff, Manager]] = []

   def add_employee(self, employee):
       if employee.role not in STAFF_ROLES:
           raise ValueError(f"Rôle invalide. Possibles : {STAFF_ROLES}")
       if employee.phone and not validate_phone(employee.phone):
           raise ValueError(f"Numéro de téléphone invalide : {employee.phone}")
       if employee.phone and self.get_by_phone(employee.phone):
           raise ValueError(f"Ce numéro est déjà utilisé : {employee.phone}")
       self.employees.append(employee)

   def remove_employee(self, name):
       for i, emp in enumerate(self.employees):
           if emp.name.lower() == name.lower():
               self.employees.pop(i)
               return True
       return False

   def get_by_role(self, role):
       if role not in STAFF_ROLES:
           return []
       return [e for e in self.employees if e.role == role]

   def get_on_shift(self):
       return [e for e in self.employees if e.is_on_shift]

   def get_by_phone(self, phone):
       for emp in self.employees:
           if emp.phone == phone:
               return emp
       return None

   def display_all_staff(self):
       if not self.employees:
           print("Aucun employé enregistré.")
           return
       print("\n" + "═" * 60)
       print("PERSONNEL DU RESTAURANT".center(60))
       print("═" * 60)
       for emp in self.employees:
           print(emp.get_info())

   def calculate_total_payroll(self):
       return sum(emp.salary for emp in self.employees)

   def save(self):
       file_handler.save_staff_to_csv(self.employees)

   def load(self):
       data = file_handler.load_staff_from_csv()
       self.employees = []
       for row in data:
           emp = Staff(
               name=row["name"],
               role=row["role"],
               salary=float(row["salary"]),
               phone=row["phone"],
               is_on_shift=row.get("is_on_shift", "False") == "True"
           )
           self.employees.append(emp)
       print(f"{len(self.employees)} employés chargés.")

   def get_all(self):
       return self.employees.copy()
