from src.cart import calculate_cart_total


def test_cart_total():
    assert calculate_cart_total(100, 2, 10) == 180


def test_cart_without_discount():
    assert calculate_cart_total(100, 2) == 200