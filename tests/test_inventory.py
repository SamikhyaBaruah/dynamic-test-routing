from src.inventory import check_stock


def test_stock_available():
    assert check_stock(10, 5) is True


def test_stock_not_available():
    assert check_stock(3, 5) is False