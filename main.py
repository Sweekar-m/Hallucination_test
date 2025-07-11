import json
import time
import threading
from First_Layer.create_ops import create_ops
from First_Layer.os_action_ops import os_action_ops

def handle_create_ops(user_input):
    create_ops(user_input)

def handle_os_action_ops(user_input):
    os_action_ops(user_input)

def main():
    with open("test_case2.json", "r") as f:
        test_cases = json.load(f)

    for case in test_cases:
        user_input = case["user_input"]
        print(f"🔹 Processing: {user_input}")

        t1 = threading.Thread(target=handle_create_ops, args=(user_input,))
        t2 = threading.Thread(target=handle_os_action_ops, args=(user_input,))

        t1.start()
        t2.start()

        t1.join()
        t2.join()

        time.sleep(20)  # Optional: small delay between batches

if __name__ == "__main__":
    main()
