"""Unit tests for main CLI application."""

import pytest
from billing import Cart, Inventory
import main


def test_seed_inventory():
    inventory = Inventory()
    main.seed_inventory(inventory)
    items = inventory.list_items()
    assert len(items) == 5
    assert items[0].name == "Apple"


def test_view_catalog(capsys):
    inventory = Inventory()
    main.seed_inventory(inventory)
    main.view_catalog(inventory)
    captured = capsys.readouterr().out
    assert "--- Inventory Catalog ---" in captured
    assert "Apple" in captured


def test_add_to_cart(monkeypatch, capsys):
    inventory = Inventory()
    main.seed_inventory(inventory)
    cart = Cart()

    # Input product ID 1, qty 2
    inputs = iter(["1", "2"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    main.add_to_cart(inventory, cart)
    captured = capsys.readouterr().out
    assert "Success: Added 2 x 'Apple' to cart." in captured
    assert 1 in cart.items
    assert cart.items[1].quantity == 2


def test_remove_from_cart(monkeypatch, capsys):
    inventory = Inventory()
    main.seed_inventory(inventory)
    cart = Cart()
    item = inventory.get_item(1)
    cart.add_item(item, 3)

    # Input item ID 1, remove qty 1
    inputs = iter(["1", "1"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    main.remove_from_cart(cart)
    captured = capsys.readouterr().out
    assert "Success: Updated cart item quantity." in captured
    assert cart.items[1].quantity == 2


def test_apply_discount(monkeypatch, capsys):
    cart = Cart()
    monkeypatch.setattr("builtins.input", lambda _: "15")

    main.apply_discount(cart)
    captured = capsys.readouterr().out
    assert "Success: Applied 15.0% discount to cart." in captured
    assert cart.discount_percent == 15.0


def test_checkout(monkeypatch, capsys):
    inventory = Inventory()
    main.seed_inventory(inventory)
    cart = Cart()
    cart.add_item(inventory.get_item(1), 1)

    monkeypatch.setattr("builtins.input", lambda _: "y")
    main.checkout(cart)
    captured = capsys.readouterr().out
    assert "BILLING RECEIPT" in captured
    assert "Checkout complete. Cart reset for next customer." in captured
    assert len(cart.items) == 0


def test_add_product_to_inventory(monkeypatch, capsys):
    inventory = Inventory()
    inputs = iter(["Orange", "2.99", "Groceries"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    main.add_product_to_inventory(inventory)
    captured = capsys.readouterr().out
    assert "Success: Added 'Orange'" in captured
    assert len(inventory.list_items()) == 1


def test_main_exit(monkeypatch, capsys):
    # Option 8 is Exit
    monkeypatch.setattr("builtins.input", lambda _: "8")
    with pytest.raises(SystemExit) as exc_info:
        main.main()
    assert exc_info.value.code == 0
    captured = capsys.readouterr().out
    assert "Thank you for using the Menu Driven Billing System." in captured
