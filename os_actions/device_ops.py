import os
import sys
import subprocess
from google import genai
import json
from create_action.json_load import save_json_safely
import re
def clean_response(text):
    # Remove markdown code block markers
    text = re.sub(r"```(json)?", "", text).strip()

    # Extract first valid JSON object from the text
    match = re.search(r"\{[\s\S]*?\}", text)
    return match.group() if match else text

def device_ops(user_msg):
    system_prompt = '''
You are SoulOS's strict intent classifier.

Your job is to classify the user_input based only on *clearly stated device-related system control commands*.

🎯 Instructions:
- Match only if the user_input includes clear and direct phrases like:
  - “eject usb”
  - “restart the system”
  - “show battery info”
- These must map to *exact intents* under the correct cluster (device_ops).
- Do NOT infer, assume, or guess user intention.
- If no intent clearly matches, return unknown confidently.

---

🎯 Intent List (device_ops cluster):

- eject_usb  
- check_battery_status  
- show_storage_info  
- open_device_manager  
- restart_system  
- shutdown_system  
- sleep_mode  
- hibernate_system  
- lock_screen  
- log_out  

---

🧠 Output Format:

✅ If matched:
```json
{
  "cluster": "device_ops",
  "intent": "<matched_intent_name>",
  "user_input": "<original_user_input>"
}


'''

    # Append user input to the content
    full_prompt = f"{system_prompt}\n\nuser_input: {user_msg}\nRespond with the correct JSON:"

    client = genai.Client(api_key="AIzaSyA8m0AoPKzANNjn1c6Y0l1WQr0lSzapMMk")
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=full_prompt
    )


    response_text = clean_response(response.text)
    save_json_safely(response_text)