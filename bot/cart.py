carts: dict[int, list] = {}

def add_to_cart(user_id: int, item: dict):
    if user_id not in carts:
        carts[user_id] = []
    carts[user_id].append(item)

def get_cart(user_id: int) -> list:
    return carts.get(user_id, [])

def clear_cart(user_id: int):
    carts[user_id] = []

def remove_from_cart(user_id: int, index: int):
    if user_id in carts and 0 <= index < len(carts[user_id]):
        carts[user_id].pop(index)

def cart_count(user_id: int) -> int:
    return len(carts.get(user_id, []))
