# 🍽️ Taste of Africa — Restaurant Management System

> **Group Project — Python I**  
> Restaurant: *Taste of Africa*, Ouagadougou, Burkina Faso

---

## 📋 Table of Contents

1. [Project Overview](#-project-overview)
2. [Features](#-features)
3. [Architecture & File Structure](#-architecture--file-structure)
4. [Module Details](#-module-details)
5. [Installation & Launch](#-installation--launch)
6. [Usage](#-usage)
7. [Data Model](#-data-model)
8. [Team & Contributions](#-team--contributions)

---

## 🌍 Project Overview

**Taste of Africa** is a restaurant management system built entirely in **Python**, developed as an academic group project. It allows a restaurant team to manage their daily operations including:

- The **menu** (dishes, drinks, availability)
- Customer **orders** (creation, tracking, billing)
- **Tables** (assignment, release, status)
- **Staff** (employees, shift tracking, payroll)
- Daily **reports** (revenue, statistics)

The project applies the core principles of **Object-Oriented Programming (OOP)**: inheritance, encapsulation, polymorphism, and abstraction. It also integrates **data persistence** through JSON and CSV files.

---

## ✨ Features

### 🥘 Menu Management
- Add dishes (`Dish`) with ingredients and preparation time
- Add drinks (`Drink`) with volume and alcoholic/non-alcoholic flag
- Display full menu sorted by category (starters, main courses, desserts, drinks)
- Manage item availability
- Automatic save to JSON

### 📝 Order Management
- Create an order linked to a table and a server
- Add items (dishes or drinks) with quantity
- Track order status: `waiting` → `in preparation` → `served` → `paid` / `cancelled`
- Automatic subtotal and total calculation including VAT (18%)
- Print detailed receipt
- Persistent storage of closed orders in JSON

### 🪑 Table Management
- 15 configured tables (capacity: 4 people each)
- Assign a table to a customer
- Automatic release when an order is closed
- View the status of all tables at a glance

### 👥 Staff Management
- Four roles: `server`, `chef`, `manager`, `cashier`
- Clock in / clock out tracking
- Search by role or phone number
- Calculate total payroll
- Save and load from CSV file

### 📊 Reports
- Daily report: revenue, staff on shift, menu item count
- Full receipt with subtotal, VAT and total
- Simplified receipt for quick printing

---

## 🗂️ Architecture & File Structure

```
Taste-of-Africa/
│
├── main.py              # Entry point — main application loop
├── constants.py         # Global configuration (name, VAT, currency, paths)
├── models.py            # Business classes (Person, Staff, MenuItem, Order, Table…)
├── menu.py              # MenuManager — menu handling
├── Orders.py            # OrderManager + TableManager
├── Staff.py             # StaffManager — staff handling
├── repports.py          # Report and receipt generation
├── ui.py                # Console interface (menus, user input)
├── utils.py             # Utility functions (ID generation, formatting, validation)
├── file_handler.py      # Persistence: JSON and CSV read/write
│
└── data/                # Persistent data files (auto-generated at runtime)
    ├── menu.json        # Saved menu
    ├── orders.json      # Order history
    └── staff.csv        # Staff list
```

---

## 🔍 Module Details

### `constants.py`
Centralises all application configuration:
- Restaurant name and address
- VAT rate (18%), currency (XOF / F CFA)
- Paths to data files
- Immutable tuples for order statuses, staff roles, and menu categories

### `models.py`
The core of the project — contains the full class hierarchy:

| Class | Inherits from | Role |
|---|---|---|
| `Person` | — | Base class (name, phone) |
| `Customer` | `Person` | Customer with table number and order history |
| `Staff` | `Person` | Employee with role, salary and shift status |
| `Manager` | `Staff` | Manager with team and department |
| `MenuItem` | — | Menu item (id, name, price, category) |
| `Dish` | `MenuItem` | Dish with ingredients and prep time |
| `Drink` | `MenuItem` | Drink with volume and alcohol indicator |
| `Order` | — | Order with items, status and timestamp |
| `Table` | — | Table with capacity and occupation state |

### `menu.py`
`MenuManager` handles the list of menu items. It provides:
- Add, remove, search by ID or category
- Filter available items
- Formatted display by category
- Delegates save/load to `file_handler`

### `Orders.py`
Two complementary classes:
- **`OrderManager`**: creates, tracks and closes active orders; loads and saves history to JSON
- **`TableManager`**: manages table states (occupied/free) and assigns them to customers

### `Staff.py`
`StaffManager` manages the employee list:
- Validates role and phone number on add
- Detects phone number duplicates
- Filter by role or shift status
- CSV persistence via `file_handler`

### `repports.py`
Reporting functions:
- `generate_daily_report()`: complete daily report (revenue, staff, menu)
- `print_receipt()`: detailed receipt with VAT, totals and restaurant info
- `print_simple_receipt()`: lightweight version for quick printing

### `ui.py`
Interactive console interface:
- Main menu and submenus for each module
- Typed user input with validation and error messages
- Confirmation prompts for critical actions (close order, quit)

### `utils.py`
Reusable utility functions:
- `generate_id(prefix)`: generates a unique timestamped ID (e.g. `CMD-143022-AKZ`)
- `format_currency(amount)`: monetary formatting in XOF
- `validate_phone(phone)`: phone number validation (8 to 12 digits)
- `print_header()` / `print_separator()`: console formatting helpers

### `file_handler.py`
Data access layer:
- Save and load menu as **JSON**
- Save and load staff as **CSV**
- Automatic creation of the `data/` folder if missing
- I/O error handling

---

## 🚀 Installation & Launch

### Prerequisites
- Python **3.10** or higher (uses `X | Y` union type syntax)
- No external dependencies — Python standard library only

### Setup

```bash
# Clone the repository
git clone https://github.com/Hassanecbl0/Restauration-Project.git
cd Restauration-Project

# Run the application
python main.py
```

The `data/` folder and persistence files are created automatically on first launch.

---

## 🖥️ Usage

On startup, the application loads existing data and displays the main menu:

```
════════════════════════════════════════════════════════════
         Taste of Africa - MANAGEMENT SYSTEM
════════════════════════════════════════════════════════════
  1. Menu management
  2. Order management
  3. Table management
  4. Staff management
  5. Reports & statistics
  0. Quit the program
────────────────────────────────────────────────────────────
Your choice →
```

### Typical order workflow
1. **Table management** → Assign a table to a customer
2. **Order management** → Create a new order (table + server)
3. **Order management** → Add items from the menu
4. **Order management** → Close and bill the order (receipt printed + table released)

---

## 🗃️ Data Model

### Order status flow
```
waiting → in preparation → served → paid
                                 ↘ cancelled
```

### Menu categories
`starter` | `main course` | `dessert` | `drink`

### Staff roles
`server` | `chef` | `manager` | `cashier`

### Sample generated receipt
```
════════════════════════════════════════════════════════════
              RECEIPT — Order #CMD-143022-AKZ
════════════════════════════════════════════════════════════
  Table  : 3
  Server : Fatima Sawadogo
  Date   : 2026-05-30 14:30
  Status : WAITING
────────────────────────────────────────────────────────────
  Rice with peanut sauce       x 2       5,000 XOF
  Bissap juice                 x 1         800 XOF
────────────────────────────────────────────────────────────
  Subtotal                               5,800 XOF
  VAT (18%)                              1,044 XOF
────────────────────────────────────────────────────────────
  TOTAL                                  6,844 XOF
════════════════════════════════════════════════════════════
              Thank you for your visit !
              Ouagadougou, Burkina Faso
════════════════════════════════════════════════════════════
```

---

## 👨‍💻 Team & Contributions

This project was built by a team of 6 members, each responsible for a specific module.

---

### 👤 Member 1 — Project Lead
**Files:** `constants.py` · `utils.py` · `README.md` · GitHub coordination

Responsible for the global project configuration, shared constants used across all modules, common utility functions, and GitHub repository coordination (branches, integration, code review).

🔗 [https://github.com/Hassanecbl0](https://github.com/Hassanecbl0)

---

### 👤 Member 2 — OOP & Models
**Files:** `models.py` *(largest and most complex file)*

Responsible for the entire object-oriented class hierarchy: `Person`, `Customer`, `Staff`, `Manager`, `MenuItem`, `Dish`, `Drink`, `Order` and `Table`. Designed encapsulation, properties, inheritance and serialization methods (`to_dict` / `from_dict`).

🔗 [https://github.com/CNoura-spec](https://github.com/CNoura-spec)

---

### 👤 Member 3 — Menu & Orders
**Files:** `menu.py` · `Orders.py`

Responsible for the business logic of the menu and orders. Developed `MenuManager` (add, search, category display, save) and `OrderManager` + `TableManager` (order lifecycle, table management, JSON persistence).

🔗 [https://github.com/laurenciabonkougou](https://github.com/laurenciabonkougou)

---

### 👤 Member 4 — Staff & Reports
**Files:** `Staff.py` · `repports.py`

Responsible for staff management (`StaffManager`: add, validation, role filtering, payroll calculation, CSV persistence) and report generation (`generate_daily_report`, `print_receipt`, `print_simple_receipt`).

🔗 [https://github.com/wendyhack07](https://github.com/wendyhack07)

---

### 👤 Member 5 — Files & Data
**Files:** `file_handler.py` · `data/menu.json` · `data/orders.txt` · `data/staff.csv`

Responsible for the entire data persistence layer: reading and writing JSON files (menu, orders) and CSV files (staff), I/O error handling, automatic `data/` directory creation, and data integrity across sessions.

🔗 [https://github.com/Aubin0103](https://github.com/Aubin0103)

---

### 👤 Member 6 — Interface & Integration
**Files:** `ui.py` · `main.py` *(ties all modules together)*

Responsible for the console interface (menus, input handling, confirmations) and the main `main.py` file that orchestrates all modules: initialization, main loop, submenu routing, and dependency injection between managers.

🔗 [https://github.com/bombirigael1-lang](https://github.com/bombirigael1-lang)

---
# Restauration-Project-
