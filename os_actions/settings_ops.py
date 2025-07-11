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
def settings_ops(user_msg):
    system_prompt = '''
You are SoulOS's strict intent classifier.

Your job is to classify the user_input based only on *clearly stated system settings adjustment commands*.

🎯 Instructions:
- Match only if the user_input contains clear phrases like:
  - “change wallpaper”
  - “adjust volume”
  - “enable bluetooth”
  - “set brightness to 70”
- Do NOT infer or interpret — classify only if the command is explicit.

---

🎯 Intent List (settings_ops cluster):

- change_wallpaper  
- adjust_volume  
- change_theme  
- toggle_dark_mode  
- set_brightness  
- update_timezone  
- enable_bluetooth  
- disable_wifi  
- set_default_browser  
- configure_notifications  

---

🧠 Output Format:

✅ If matched:
```json
{
  "cluster": "settings_ops",
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