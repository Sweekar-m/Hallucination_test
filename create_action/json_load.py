import json
import os

def save_json_safely(json_str):
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError:
        print("Invalid JSON format. Skipped.")
        return

    # Load existing data or start a new list
    if os.path.exists("result.json"):
        with open("result.json", "r") as f:
            try:
                existing_data = json.load(f)
                if not isinstance(existing_data, list):
                    existing_data = []
            except json.JSONDecodeError:
                existing_data = []
    else:
        existing_data = []

    # Append new entry
    existing_data.append(data)

    # Save back to file
    with open("result.json", "w") as f:
        json.dump(existing_data, f, indent=2)

    print("Appended to result.json")