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
def screen_ops(user_msg):
    system_prompt = '''
You are SoulOS's strict intent classifier.

Your job is to classify the user_input based only on *clearly stated screen-related control commands*.

🎯 Instructions:
- Match only if the user_input includes clear commands like:
  - “take a screenshot”
  - “start screen recording”
  - “enable night light”
  - “mirror my screen”
- Do NOT guess or infer — match only when the action is explicit.

---

🎯 Intent List (screen_ops cluster):

- take_screenshot  
- record_screen  
- stop_recording  
- start_live_stream  
- toggle_screen_share  
- open_display_settings  
- rotate_screen  
- enable_night_light  
- disable_night_light  
- mirror_screen  

---

🧠 Output Format:

✅ If matched:
```json
{
  "cluster": "screen_ops",
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