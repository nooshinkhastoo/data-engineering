import redis

r = redis.Redis(
    host="redis",
    port=6379,
    decode_responses=True,
)

pubsub = r.pubsub()

pubsub.subscribe("order-events")

print("Notification service started", flush=True)

for message in pubsub.listen():

    if message["type"] == "message":
        print(
            f"Received event: {message['data']}",
            flush=True
        )