from Utils.config import CATEGORIES, UNITS
import os
import time
import json

class PantryItem:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # path to /Pantry
    filepath = os.path.normpath(os.path.join(BASE_DIR, '..', 'Data', 'pantry.json'))

    def __init__(self):
        self.name = ""
        self.category = ""
        self.quantity : 0
        self.unit = ""
        self._load_items()


    def _get_category_list(self):
        categories = CATEGORIES
        print("=" * 50)
        print("\n Choose category: ")
        for key, val in categories.items():
            print(f"{key}. {val}")

        while True:
            selected_category = input("\n Select category: ")
            if selected_category in categories:
                return categories[selected_category]
            else:
                print("❌ Invalid choice. Please select a valid number from the list.")



    def _get_unit_list(self):
        units = UNITS
        print("-"*50)
        print("\n Choose unit")        
        for key,val in units.items():
            print(f"{key}. {val}")

        while True:
            selected_unit = input("\n Select unit: ")
            if selected_unit in units:
                return units[selected_unit]
            else:
                print("❌ Invalid choice. Please select a valid number from the list.")            

        
    def _validate_quantity(self):
        quantity = input("Enter quantity: ")
        try:
            return float(quantity) if '.' else int(quantity)
        except ValueError:
            print("❌ Invalid input. Please enter a valid number.")


    def _save_item(self):
        ## Write to JSON file
        try:
            with open(self.filepath,"w+") as file:
                json.dump(self.items, file, indent=4)

            print("✅ Transactions saved successfully.")

        except FileNotFoundError:
            print("❌ File path not found.")
        except Exception as e:
            print(f"❌ An error occurred while saving transactions: {e}")
      

    def add_item(self):
        record = {}
        self.name = input("Enter the item name : ")
        self.category = self._get_category_list()
        self.quanity = self._validate_quantity()
        self.unit = self._get_unit_list()
        self.date_added = time.strftime("%Y-%m-%d")

        # create the item dictionary
        record = {
            "name": self.name,
            "category" : self.category,
            "quantity" : self.quanity,
            "unit" : self.unit,
            "date_added" : self.date_added
        }
        self.items.append(record)
        
        # Saving the record in the json file
        self._save_item()


    def _load_items(self):
        try:
            if os.path.exists(self.filepath) and os.path.getsize(self.filepath) > 0:
                with open(self.filepath,"r") as file:
                    content = json.load(file)
                    self.items = content
            else:
                self.items = []
        except json.JSONDecodeError:
            print("❌ Error: records.json contains invalid JSON.")

    
    def view_items(self):
        self._load_items()  # Always load the latest items first

        if self.items:
            print("\n📦 Current Pantry Items:")
            print("-" * 100)
            print(f"{'No.':<4} {'Name':<25} {'Category':<25} {'Quantity':<15} {'Unit':<15} {'Date Added':<10}")
            print("-" * 100)
            for i, item in enumerate(self.items, start=1):
                print(f"{i:<4} {item.get('name', ''):<25} {item.get('category', ''):<25} "
                    f"{item.get('quantity', 0):<15.2f} {item.get('unit', ''):<15} {item.get('date_added', ''):<10}")
            print("-" * 100)
        else:
            print("🟡 No items found in pantry.")


    
    def delete_item(self):
        self._load_items()  # ✅ Fix: Add parentheses

        # Assuming you have or will create a view_items() method
        self.view_items()

        if not self.items:
            print("🟡 Pantry is empty. Nothing to delete.")
            return

        while True:
            try:            
                item_no = int(input("\n🗑️  Enter the item number to delete: "))
                if 1 <= item_no <= len(self.items):
                    deleted = self.items.pop(item_no - 1)
                    self._save_item()
                    print(f"✅ '{deleted['name']}' has been removed from your pantry.")
                    break  # ✅ Exit loop after successful deletion
                else:
                    print("❌ Invalid item number.")
            except ValueError:
                print("❌ Please enter a valid number.")





        
