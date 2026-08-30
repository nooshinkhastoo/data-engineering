import redis
import time

r = redis.Redis(
    host="redis",
    port=6379,
    decode_responses=True,
    socket_timeout=None,
)

print("Worker started", flush=True)

while True:
    result = r.blpop("orders:queue", timeout=0)

    if result:
        _, order_key = result

        print(f"Processing {order_key}", flush=True)

        r.hset(order_key, "status", "processing")

        time.sleep(2)

        r.hset(order_key, "status", "completed")

        r.publish(
            "order-events",
            f"{order_key} completed"
        )

        print(f"Completed {order_key}", flush=True)