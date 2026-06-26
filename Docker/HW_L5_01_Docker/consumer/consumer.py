import os
import time

log_file = "/shared/app.log"
error_file = "/shared/errors.log"

while not os.path.exists(log_file):
    print("Waiting for log file...")
    time.sleep(1)

with open(log_file, "r") as f:
    f.seek(0, 2) 

    while True:
        line = f.readline()

        if not line:
            time.sleep(1)
            continue

        line = line.strip()
        print("NEW:", line)

        if "ERROR" in line or "WARNING" in line:
            with open(error_file, "a") as ef:
                ef.write(line + "\n")