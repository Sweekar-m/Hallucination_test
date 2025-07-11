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
def network_ops(user_msg):
    system_prompt = '''
You are SoulOS's strict intent classifier.

Your job is to classify the user_input based only on *clearly stated network-related commands*.

🎯 Instructions:
- Match only if the user_input contains direct phrases like:
  - “connect to wifi”
  - “ping google”
  - “reset my network”
  - “show available networks”
- Only classify if intent is *clearly* stated — no guessing or assumptions.

---

🎯 Intent List (network_ops cluster):

- connect_wifi  
- disconnect_wifi  
- check_ip  
- ping_google  
- enable_airplane_mode  
- disable_airplane_mode  
- reset_network  
- open_network_settings  
- show_wifi_list  
- troubleshoot_network  

---

🧠 Output Format:

✅ If matched:
```json
{
  "cluster": "network_ops",
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