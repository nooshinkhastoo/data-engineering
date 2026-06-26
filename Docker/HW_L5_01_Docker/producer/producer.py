import os
import time
import random
from datetime import datetime

interval = int(os.getenv("LOG_INTERVAL", 2))

levels = ["INFO", "WARNING", "ERROR"]

messages = {
    "INFO": ["User logged in", "File uploaded"],
    "WARNING": ["Disk usage is high"],
    "ERROR": ["Database connection failed"]
}

seq = 1

while True:
    level = random.choice(levels)
    msg = random.choice(messages[level])
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log = f"{time_now} | {level} | #{seq} | {msg}"

    with open("/shared/app.log", "a") as f:
        f.write(log + "\n")

    print(log)

    seq += 1
    time.sleep(interval)