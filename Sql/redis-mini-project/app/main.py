import redis

r = redis.Redis(
    host="redis",
    port=6379,
    decode_responses=True,
)


def create_order(order_id, customer_id, product_id, quantity):
    order_key = f"order:{order_id}"

    # 1. Store order information in a Hash
    r.hset(
        order_key,
        mapping={
            "customer_id": customer_id,
            "product_id": product_id,
            "quantity": quantity,
            "status": "pending",
        },
    )

    # 2. Add order to the processing queue
    r.lpush("orders:queue", order_key)

    # 3. Increment total order counter
    total_orders = r.incr("orders:count")

    return total_orders


print("Redis connection:", r.ping())

total = create_order(
    order_id=1001,
    customer_id=50,
    product_id=123,
    quantity=2,
)

print("Total orders:", total)