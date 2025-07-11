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
def system_ops(user_msg):
    system_prompt = '''
You are SoulOS's strict intent classifier.

Your job is to classify the user_input based only on *clearly stated system application launch commands*.

🎯 Instructions:
- Match only if the user_input includes explicit phrases like:
  - “open calculator”
  - “launch notepad”
  - “start command prompt”
  - “open file explorer”
- Match only when the intent is unambiguous and exact — no guessing or assumptions.

---

🎯 Intent List (system_ops cluster):

- open_calculator  
- open_notepad  
- open_cmd  
- open_task_manager  
- open_settings  
- open_control_panel  
- open_file_explorer  
- open_snipping_tool  
- open_browser  
- open_terminal  

---

🧠 Output Format:

✅ If matched:
```json
{
  "cluster": "system_ops",
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