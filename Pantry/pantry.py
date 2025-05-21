import os
import json
import time
from Utils.config import CATEGORIES, UNITS

class PantryItem:
    def __init__(self, name, category, quantity, unit, date_added, last_updated=None):
        self.name = name
        self.category = category
        self.quantity = quantity  # Triggers @property setter
        self.unit = unit
        self.date_added = date_added
        self.last_updated = last_updated or date_added

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        val = float(value)
        if val < 0:
            raise ValueError("❌ Quantity cannot be negative.")
        self._quantity = val
        self.last_updated = time.strftime("%Y-%m-%d")

    def to_dict(self):
        return {
            "name": self.name,
            "category": self.category,
            "quantity": self.quantity,
            "unit": self.unit,
            "date_added": self.date_added,
            "last_updated": self.last_updated
        }

    @staticmethod
    def from_dict(data):
        return PantryItem(
            name=data["name"],
            category=data["category"],
            quantity=data["quantity"],
            unit=data["unit"],
            date_added=data["date_added"],
            last_updated=data.get("last_updated")
        )


class PantryManager:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    FILE_PATH = os.path.normpath(os.path.join(BASE_DIR, '..', 'Data', 'pantry.json'))

    def __init__(self):
        self.items = self._load_items()

    def _load_items(self):
        try:
            if os.path.exists(self.FILE_PATH) and os.path.getsize(self.FILE_PATH) > 0:
                with open(self.FILE_PATH, "r") as file:
                    data = json.load(file)
                    return [PantryItem.from_dict(item) for item in data]
        except json.JSONDecodeError:
            print("❌ Error: pantry.json contains invalid JSON.")
        return []

    def _save_items(self):
        try:
            with open(self.FILE_PATH, "w") as file:
                json.dump([item.to_dict() for item in self.items], file, indent=4)
            print("✅ Pantry items saved successfully.")
        except Exception as e:
            print(f"❌ Failed to save pantry items: {e}")

    def add_item(self):
        print("\n📥 Add New Pantry Item")
        print("-"*30)
        name = input("Enter item name: ")
        category = self._choose_from_dict("category", CATEGORIES)
        quantity = self._validate_quantity()
        unit = self._choose_from_dict("unit", UNITS)
        date_added = time.strftime("%Y-%m-%d")

        item = PantryItem(name, category, quantity, unit, date_added)
        self.items.append(item)
        self._save_items()

    def view_items(self):
        if not self.items:
            print("\n🟡 No items in pantry.")
            return

        print("\n📦 Pantry Items:")
        print("-" * 105)
        print(f"{'No.':<4} {'Name':<25} {'Category':<20} {'Quantity':<10} {'Unit':<10} {'Date Added':<15} {'Last Updated':<15}")
        print("-" * 105)

        for i, item in enumerate(self.items, start=1):
            print(f"{i:<4} {item.name:<25} {item.category:<20} {item.quantity:<10.2f} {item.unit:<10} "
                  f"{item.date_added:<15} {item.last_updated:<15}")
        print("-" * 105)

    def update_item(self):
        self.view_items()
        if not self.items:
            return

        try:
            idx = int(input("\n✏️  Enter item number to update quantity: ")) - 1
            if 0 <= idx < len(self.items):
                new_qty = self._validate_quantity()
                self.items[idx].quantity = new_qty
                self._save_items()
                print(f"✅ Quantity updated for '{self.items[idx].name}'.")
            else:
                print("❌ Invalid item number.")
        except ValueError:
            print("❌ Invalid input. Please enter a number.")

    def delete_item(self):
        self.view_items()
        if not self.items:
            return

        try:
            idx = int(input("\n🗑️  Enter item number to delete: ")) - 1
            if 0 <= idx < len(self.items):
                deleted = self.items.pop(idx)
                self._save_items()
                print(f"✅ Deleted '{deleted.name}' from pantry.")
            else:
                print("❌ Invalid item number.")
        except ValueError:
            print("❌ Invalid input. Please enter a number.")

    def _choose_from_dict(self, label, options):
        print(f"\nChoose {label}:")
        for key, val in options.items():
            print(f"{key}. {val}")
        while True:
            choice = input(f"Enter {label} number: ")
            if choice in options:
                return options[choice]
            print(f"❌ Invalid {label}. Try again.")

    def _validate_quantity(self):
        while True:
            try:
                qty = float(input("Enter quantity: "))
                if qty < 0:
                    raise ValueError
                return qty
            except ValueError:
                print("❌ Please enter a valid non-negative number.")
