from typing import List, Optional
from models import MenuItem, Dish, Drink
from constants import MENU_CATEGORIES
import file_handler
class MenuManager:
    def __init__(self) -> None:
        self.items: List[MenuItem] = []
    def add_item(self, item: MenuItem) -> None:
        self.__items.append(item)
    def remove_item(self, item_id:str) -> bool:
        for i, item in enumerate(self.__items):
            if item.item_id == item_id:
                self.__items.pop(i)
                return True
        return False
    def get_item_by_id(self, item_id: str) -> Optional [MenuItem]:
        for item in self.__items:
            if item.item_id == item_id:
                return item
        return None
    def get_item_by_category(self, category: str) ->List[MenuItem]:
        if category not in MENU_CATEGORIES:
            return[]
        else:
            return[item for item in self.__items if item.available]
    def get_available_items(self) -> List[MenuItem]:
        return[item for item in self.__items if item.available] 
    def display_full_menu(self) -> None:
        print("/n" + "=" * 60)
        print("RESTAURANT MENU".center(60))
        print("=" * 60)
        for category in MENU_CATEGORIES:
            items = self.get_item_by_category(category)
            if items:
                print(f"\n {category.upper()}")
                print(" " + "-" * 40)
                for item in items:
                    print(f" {item.display()}")
    def save(self) -> None:
        file_handler.save_menu_to_json(self.__items)
    def load(self) -> None:
        data = file_handler.load_menu_from_json()
        self.__items.clear()
        for item_data in data:
            if item_data.get("type") == "dish":
                self.__items.append(Dish(
                    item_id = item_data["id"],
                    name = item_data["name"],
                    price = item_data["price"],
                    category = item_data["category"],
                    ingredients = item_data.get("ingredients", []),
                    prep_time = item_data.get("prep_time", 0)
                ))
            elif item_data.get("type") == "drink":
                self.__items.append(Drink(
                    item_id = item_data["id"],
                    name = item_data["name"],
                    price = item_data["price"],
                    volume_ml = item_data.get("volume_ml", 0),
                    alcoholic = item_data.get("alcoholic", False)
                ))
            else:
                self.__items.append(MenuItem(
                    item_id = item_data["id"],
                    name = item_data["name"],
                    price = item_data["price"],
                    category = item_data["category"]
                ))
    def get_all_items(self) -> List[MenuItem]:
        return self.__items.copy()

       
        
        