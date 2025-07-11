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
def search_ops(user_msg):
    system_prompt = '''
You are SoulOS's strict intent classifier.

Your job is to classify the user_input based only on *clearly stated search-related commands*.

🎯 Instructions:
- Match only if the user_input includes direct phrases like:
  - “search files”
  - “look for photos”
  - “find downloaded documents”
  - “search web”
- Do NOT assume or infer meaning — classify only when clearly stated.

---

🎯 Intent List (search_ops cluster):

- search_files  
- search_apps  
- search_web  
- search_settings  
- search_contacts  
- search_documents  
- search_downloads  
- search_photos  
- search_music  
- search_history  

---

🧠 Output Format:

✅ If matched:
```json
{
  "cluster": "search_ops",
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