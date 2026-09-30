"""Billing System Core Module.

Provides data structures and logic for inventory management, shopping cart
operations, tax and discount calculations, and receipt generation.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class Item:
    """Represents a product item in the inventory."""

    item_id: int
    name: str
    price: float
    category: str = "General"

    def __post_init__(self) -> None:
        if self.price < 0:
            raise ValueError("Price cannot be negative.")


class Inventory:
    """Manages store items and catalog."""

    def __init__(self) -> None:
        self._items: Dict[int, Item] = {}
        self._next_id: int = 1

    def add_item(self, name: str, price: float, category: str = "General") -> Item:
        """Adds a new item to the inventory."""
        item = Item(item_id=self._next_id, name=name, price=price, category=category)
        self._items[self._next_id] = item
        self._next_id += 1
        return item

    def get_item(self, item_id: int) -> Optional[Item]:
        """Retrieves an item by its ID."""
        return self._items.get(item_id)

    def remove_item(self, item_id: int) -> bool:
        """Removes an item from the inventory."""
        if item_id in self._items:
            del self._items[item_id]
            return True
        return False

    def list_items(self) -> List[Item]:
        """Returns a list of all available items."""
        return list(self._items.values())

    def update_item_price(self, item_id: int, new_price: float) -> bool:
        """Updates the price of an item."""
        if item_id in self._items:
            if new_price < 0:
                raise ValueError("Price cannot be negative.")
            self._items[item_id].price = new_price
            return True
        return False


@dataclass
class CartItem:
    """Represents an item added to the shopping cart."""

    item: Item
    quantity: int

    @property
    def total_price(self) -> float:
        return self.item.price * self.quantity


class Cart:
    """Manages customer shopping cart and billing calculations."""

    def __init__(self, tax_rate: float = 0.05, discount_percent: float = 0.0) -> None:
        self.items: Dict[int, CartItem] = {}
        self.tax_rate: float = tax_rate  # Default 5%
        self.discount_percent: float = discount_percent

    def add_item(self, item: Item, quantity: int = 1) -> None:
        """Adds an item or increments its quantity in the cart."""
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")

        if item.item_id in self.items:
            self.items[item.item_id].quantity += quantity
        else:
            self.items[item.item_id] = CartItem(item=item, quantity=quantity)

    def remove_item(self, item_id: int, quantity: Optional[int] = None) -> bool:
        """Removes an item or reduces its quantity in the cart."""
        if item_id not in self.items:
            return False

        if quantity is None or quantity >= self.items[item_id].quantity:
            del self.items[item_id]
        else:
            if quantity <= 0:
                raise ValueError("Quantity to remove must be greater than zero.")
            self.items[item_id].quantity -= quantity

        return True

    def clear(self) -> None:
        """Clears all items from the cart."""
        self.items.clear()

    def get_subtotal(self) -> float:
        """Calculates subtotal price of all cart items."""
        return sum(cart_item.total_price for cart_item in self.items.values())

    def get_discount_amount(self) -> float:
        """Calculates discount amount based on discount percentage."""
        return self.get_subtotal() * (self.discount_percent / 100.0)

    def get_tax_amount(self) -> float:
        """Calculates tax amount applied after discount."""
        taxable_amount = max(0.0, self.get_subtotal() - self.get_discount_amount())
        return taxable_amount * self.tax_rate

    def get_total(self) -> float:
        """Calculates grand total."""
        subtotal = self.get_subtotal()
        discount = self.get_discount_amount()
        tax = self.get_tax_amount()
        return subtotal - discount + tax

    def generate_receipt(self) -> str:
        """Generates a formatted receipt string."""
        lines = []
        lines.append("=" * 45)
        lines.append(f"{'BILLING RECEIPT':^45}")
        lines.append("=" * 45)
        lines.append(f"{'Item Name':<20} {'Qty':<5} {'Price':<8} {'Total':<8}")
        lines.append("-" * 45)

        for cart_item in self.items.values():
            item_name = cart_item.item.name[:18]
            qty = cart_item.quantity
            price = f"${cart_item.item.price:.2f}"
            total = f"${cart_item.total_price:.2f}"
            lines.append(f"{item_name:<20} {qty:<5} {price:<8} {total:<8}")

        lines.append("-" * 45)
        subtotal = self.get_subtotal()
        discount = self.get_discount_amount()
        tax = self.get_tax_amount()
        grand_total = self.get_total()

        lines.append(f"{'Subtotal:':<34} ${subtotal:>8.2f}")
        if self.discount_percent > 0:
            lines.append(f"{f'Discount ({self.discount_percent:.1f}%):':<34} -${discount:>7.2f}")
        lines.append(f"{f'Tax ({self.tax_rate * 100:.1f}%):':<34} ${tax:>8.2f}")
        lines.append("=" * 45)
        lines.append(f"{'GRAND TOTAL:':<34} ${grand_total:>8.2f}")
        lines.append("=" * 45)
        lines.append(f"{'Thank you for your business!':^45}")
        lines.append("=" * 45)

        return "\n".join(lines)
