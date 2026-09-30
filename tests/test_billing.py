"""Unit tests for billing core module."""

import pytest
from billing import Cart, Inventory, Item


def test_item_creation():
    item = Item(item_id=1, name="Test Item", price=10.0, category="Test")
    assert item.item_id == 1
    assert item.name == "Test Item"
    assert item.price == 10.0
    assert item.category == "Test"

    with pytest.raises(ValueError):
        Item(item_id=2, name="Bad Item", price=-5.0)


def test_inventory_operations():
    inv = Inventory()
    item1 = inv.add_item("Apple", 1.5, "Fruit")
    item2 = inv.add_item("Banana", 0.75, "Fruit")

    assert item1.item_id == 1
    assert item2.item_id == 2
    assert len(inv.list_items()) == 2

    assert inv.get_item(1) == item1
    assert inv.get_item(999) is None

    assert inv.update_item_price(1, 1.80) is True
    assert inv.get_item(1).price == 1.80

    with pytest.raises(ValueError):
        inv.update_item_price(1, -1.0)

    assert inv.remove_item(2) is True
    assert len(inv.list_items()) == 1
    assert inv.remove_item(2) is False


def test_cart_operations():
    inv = Inventory()
    item1 = inv.add_item("Laptop", 1000.0)
    item2 = inv.add_item("Mouse", 50.0)

    cart = Cart(tax_rate=0.10, discount_percent=10.0)
    cart.add_item(item1, 1)
    cart.add_item(item2, 2)

    assert cart.get_subtotal() == 1100.0  # 1000 + 2*50
    assert cart.get_discount_amount() == 110.0  # 10% of 1100
    # Taxable amount = 1100 - 110 = 990. Tax @ 10% = 99
    assert cart.get_tax_amount() == 99.0
    assert cart.get_total() == 1089.0  # 990 + 99

    # Partial removal
    cart.remove_item(item2.item_id, 1)
    assert cart.items[item2.item_id].quantity == 1
    assert cart.get_subtotal() == 1050.0

    # Complete removal
    cart.remove_item(item1.item_id)
    assert item1.item_id not in cart.items

    # Test error cases
    with pytest.raises(ValueError):
        cart.add_item(item2, 0)

    with pytest.raises(ValueError):
        cart.remove_item(item2.item_id, -1)

    cart.clear()
    assert len(cart.items) == 0


def test_receipt_generation():
    inv = Inventory()
    item = inv.add_item("Book", 20.0)

    cart = Cart(tax_rate=0.05, discount_percent=5.0)
    cart.add_item(item, 2)

    receipt = cart.generate_receipt()
    assert "BILLING RECEIPT" in receipt
    assert "Book" in receipt
    assert "$40.00" in receipt
    assert "Discount (5.0%):" in receipt
    assert "Tax (5.0%):" in receipt
    assert "GRAND TOTAL:" in receipt
