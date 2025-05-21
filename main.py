from Pantry.pantry import PantryManager

def main():
    print("=" * 55)
    print("🍎  Welcome to Pantry Tracker CLI!  🥫")
    print("Keep your kitchen organized — one item at a time.")
    print("=" * 55)

    is_active = True

    while is_active:
        manager = PantryManager()
        print("\n📋 MENU")
        print("-"*20)
        print("1. Add Item")
        print("2. View pantry")
        print("3. Update Item")
        print("4. Delete Item")
        print("5. Exit\n")

        selection = input("Please select from the given choices 1, 2, 3, 4 or 5 : ")

        match selection:
            case "1":
                manager.add_item()
            case "2":
                manager.view_items()
            case "3":
                manager.update_item()
            case "4":
                manager.delete_item()
            case "5":
                print("=" * 55)
                print("👋 Thank you for using Pantry Tracker. Goodbye!")
                print("=" * 55)
                is_active = False
            case _:
                print("❌ Invalid choice. Please select an option: 1, 2, 3, 4 or 5\n") 

        



if __name__ == "__main__":
    main()
