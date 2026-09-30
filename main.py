"""Menu Driven Billing System CLI Application."""

import sys
from billing import Cart, Inventory


def display_menu() -> None:
    """Displays the main menu options."""
    print("\n" + "=" * 40)
    print("      MENU DRIVEN BILLING SYSTEM      ")
    print("=" * 40)
    print(" 1. View Inventory Catalog")
    print(" 2. Add Item to Cart")
    print(" 3. Remove Item from Cart")
    print(" 4. View Shopping Cart")
    print(" 5. Apply Discount (%)")
    print(" 6. Generate Bill / Checkout")
    print(" 7. Admin: Add New Product to Inventory")
    print(" 8. Exit")
    print("=" * 40)


def seed_inventory(inventory: Inventory) -> None:
    """Populates default items into the inventory catalog."""
    inventory.add_item("Apple", 1.50, "Groceries")
    inventory.add_item("Bread", 2.50, "Bakery")
    inventory.add_item("Milk (1L)", 3.20, "Dairy")
    inventory.add_item("Coffee (250g)", 5.99, "Beverages")
    inventory.add_item("Chocolate Bar", 2.00, "Snacks")


def view_catalog(inventory: Inventory) -> None:
    """Displays all items in the inventory."""
    items = inventory.list_items()
    print("\n--- Inventory Catalog ---")
    if not items:
        print("No items available in inventory.")
        return

    print(f"{'ID':<5} {'Name':<22} {'Category':<12} {'Price':<8}")
    print("-" * 50)
    for item in items:
        print(f"{item.item_id:<5} {item.name:<22} {item.category:<12} ${item.price:.2f}")


def add_to_cart(inventory: Inventory, cart: Cart) -> None:
    """Handles adding an item to the shopping cart."""
    view_catalog(inventory)
    try:
        item_id = int(input("\nEnter Product ID to add: ").strip())
        item = inventory.get_item(item_id)
        if not item:
            print("Error: Product ID not found in catalog.")
            return

        qty_str = input(f"Enter quantity for '{item.name}': ").strip()
        qty = int(qty_str)
        if qty <= 0:
            print("Error: Quantity must be a positive integer.")
            return

        cart.add_item(item, qty)
        print(f"Success: Added {qty} x '{item.name}' to cart.")
    except ValueError:
        print("Error: Invalid numeric input.")


def remove_from_cart(cart: Cart) -> None:
    """Handles removing an item from the shopping cart."""
    if not cart.items:
        print("\nCart is currently empty.")
        return

    view_cart(cart)
    try:
        item_id = int(input("\nEnter Product ID to remove: ").strip())
        if item_id not in cart.items:
            print("Error: Item ID is not in your cart.")
            return

        current_qty = cart.items[item_id].quantity
        qty_input = input(f"Enter quantity to remove (max {current_qty}, press Enter for all): ").strip()

        if qty_input == "":
            cart.remove_item(item_id)
            print("Success: Item removed from cart.")
        else:
            qty = int(qty_input)
            if qty <= 0:
                print("Error: Quantity must be greater than zero.")
                return
            cart.remove_item(item_id, qty)
            print("Success: Updated cart item quantity.")
    except ValueError:
        print("Error: Invalid numeric input.")


def view_cart(cart: Cart) -> None:
    """Displays the current items in the cart with subtotal."""
    print("\n--- Current Shopping Cart ---")
    if not cart.items:
        print("Your cart is empty.")
        return

    print(f"{'ID':<5} {'Name':<20} {'Qty':<5} {'Price':<8} {'Total':<8}")
    print("-" * 50)
    for cart_item in cart.items.values():
        item = cart_item.item
        print(
            f"{item.item_id:<5} {item.name:<20} {cart_item.quantity:<5} "
            f"${item.price:<7.2f} ${cart_item.total_price:<7.2f}"
        )
    print("-" * 50)
    print(f"Subtotal: ${cart.get_subtotal():.2f}")
    if cart.discount_percent > 0:
        print(f"Discount Applied: {cart.discount_percent:.1f}%")


def apply_discount(cart: Cart) -> None:
    """Allows user to specify a discount percentage."""
    try:
        discount = float(input("\nEnter discount percentage (0-100): ").strip())
        if discount < 0 or discount > 100:
            print("Error: Discount percentage must be between 0 and 100.")
            return
        cart.discount_percent = discount
        print(f"Success: Applied {discount:.1f}% discount to cart.")
    except ValueError:
        print("Error: Invalid percentage value.")


def checkout(cart: Cart) -> None:
    """Generates bill receipt and resets the cart."""
    if not cart.items:
        print("\nCannot checkout: Shopping cart is empty.")
        return

    print("\n" + cart.generate_receipt())
    confirm = input("\nComplete checkout and reset cart? (y/n): ").strip().lower()
    if confirm in ("y", "yes"):
        cart.clear()
        print("Checkout complete. Cart reset for next customer.")
    else:
        print("Receipt generated. Cart retained.")


def add_product_to_inventory(inventory: Inventory) -> None:
    """Admin function to add a new product to inventory."""
    print("\n--- Add New Product ---")
    name = input("Enter product name: ").strip()
    if not name:
        print("Error: Product name cannot be empty.")
        return

    try:
        price = float(input("Enter product price: ").strip())
        if price < 0:
            print("Error: Price cannot be negative.")
            return

        category = input("Enter category (default 'General'): ").strip()
        if not category:
            category = "General"

        item = inventory.add_item(name, price, category)
        print(f"Success: Added '{item.name}' (ID: {item.item_id}) at ${item.price:.2f}.")
    except ValueError:
        print("Error: Invalid price value.")


def main() -> None:
    """Main application loop."""
    inventory = Inventory()
    seed_inventory(inventory)
    cart = Cart(tax_rate=0.05)

    while True:
        display_menu()
        choice = input("Select an option (1-8): ").strip()

        if choice == "1":
            view_catalog(inventory)
        elif choice == "2":
            add_to_cart(inventory, cart)
        elif choice == "3":
            remove_from_cart(cart)
        elif choice == "4":
            view_cart(cart)
        elif choice == "5":
            apply_discount(cart)
        elif choice == "6":
            checkout(cart)
        elif choice == "7":
            add_product_to_inventory(inventory)
        elif choice == "8":
            print("\nThank you for using the Menu Driven Billing System. Goodbye!")
            sys.exit(0)
        else:
            print("\nError: Invalid choice. Please enter a number between 1 and 8.")


if __name__ == "__main__":
    main()
