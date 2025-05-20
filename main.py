from Pantry.pantry import PantryItem

def main():
    print("=" * 50)
    print("🍎  Welcome to Pantry Tracker CLI!  🥫")
    print("Keep your kitchen organized — one item at a time.")
    print("=" * 50)

    is_active = True

    while is_active:
        pantry = PantryItem()

        print("1. Add Item")
        print("2. View pantry")
        print("3. Update Item")
        print("4. Delete Item")
        print("5. Exit")

        selection = input("Please select from the given choices 1, 2, 3, 4 or 5 : ")

        match selection:
            case "1":
                pantry.add_item()
            case "2":
                pantry.view_items()
            case "3":
                pass
            case "4":
                pantry.delete_item()
            case "5":
                print("=" * 50)
                print("👋 Thank you for using Pantry Tracker. Goodbye!")
                print("=" * 50)
                is_active = False
            case _:
                print("❌ Invalid choice. Please select an option: 1, 2, 3, 4 or 5\n") 

        



if __name__ == "__main__":
    main()
