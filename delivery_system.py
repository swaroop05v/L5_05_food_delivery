"""Food delivery order queue manager.

Creates orders from a menu, moves them through delivery statuses,
totals the day's revenue and backs the queue up to a json file.
"""
import json
from datetime import datetime

orders = {}
menu = {}
VALID_STATUSES = ["placed", "cooking", "out_for_delivery", "delivered"]


def create_order(customer, items, order_history=None):
    """Create a new order and return its id.

    Raises ValueError if the customer/items are empty or a dish is not
    on the menu.
    """
    if order_history is None:
        order_history = []
    if not customer or not items:
        raise ValueError("order needs a customer name and at least 1 item")
    total = 0
    for item in items:
        if item not in menu:
            raise ValueError(f"unknown dish: {item}")
        total += menu[item]
    order_id = max(orders, default=0) + 1
    orders[order_id] = {
        "customer": customer,
        "items": items,
        "total": total,
        "status": "placed",
    }
    order_history.append(order_id)
    return order_id


def update_order_status(order_id, status):
    """Change the status of an order (ignores unknown ids / statuses)."""
    if order_id not in orders:
        print("No such order:", order_id)
        return
    if status not in VALID_STATUSES:
        print("Invalid status:", status)
        return
    orders[order_id]["status"] = status


def read_menu_config(file="menu.json"):
    """Load the menu from a json file, use a default menu if that fails."""
    try:
        with open(file, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError):
        data = {"pizza": 250, "burger": 150, "fries": 90, "coke": 40}
    menu.clear()
    menu.update(data)


def daily_revenue():
    """Return the total of all delivered orders."""
    revenue = 0
    for order in orders.values():
        if order["status"] == "delivered":
            revenue = revenue + order["total"]
    return revenue


def backup_orders(file="orders.json"):
    """Save the orders to a json file."""
    with open(file, "w", encoding="utf-8") as f:
        json.dump(orders, f)


def restore_orders(file="orders.json"):
    """Load the orders back from the json file."""
    with open(file, encoding="utf-8") as f:
        data = json.load(f)
    # json turns the int keys into strings so convert them back
    orders.clear()
    orders.update({int(k): v for k, v in data.items()})


def print_queue():
    """Print every order with its status and total."""
    print(f"Order queue at {datetime.now()}")
    for order_id, order in orders.items():
        print(order_id, order["customer"], order["status"],
              order["total"])


def main():
    """Run a small demo of the order queue."""
    read_menu_config()
    ids = []
    demo_orders = [
        ("Asha", ["pizza", "coke"]),
        ("Ravi", ["burger", "sushi"]),
        ("", []),
    ]
    for customer, items in demo_orders:
        try:
            ids.append(create_order(customer, items))
        except ValueError as err:
            print("Could not create order:", err)
    update_order_status(ids[0], "delivered")
    update_order_status(ids[0], "teleported")
    update_order_status(42, "delivered")
    print("Revenue today:", daily_revenue())
    backup_orders()
    restore_orders()
    print_queue()


if __name__ == "__main__":
    main()
