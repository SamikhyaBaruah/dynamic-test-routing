from src.pricing import apply_discount


def calculate_cart_total(price, quantity, discount=0):
    discounted_price = apply_discount(price, discount)
    return round(discounted_price * quantity, 2)