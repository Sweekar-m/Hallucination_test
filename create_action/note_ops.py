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
def note_ops(user_msg):
    system_prompt = '''

You are SoulOS's strict intent classifier.

Your job is to classify the `user_input` based only on **clearly stated note creation commands**.

🎯 Instructions:
- Match only if the user_input includes clear trigger words like:
  - “create a note”
  - “generate daily note”
  - “make a todo list”
  - “create quick note for ideas”
- These must map to **exact intents** (like `create_quick_note`) under the correct cluster (`note_ops`).
- Do NOT infer, assume, or be creative.
- If matched, return a JSON object with:
  - the `cluster` (note_ops),
  - the matched `intent` (e.g., create_journal_entry),
  - and the original `user_input`.
- If no intent clearly matches, return `unknown` confidently.

---

🎯 Intent List (`note_ops` cluster):

- create_note  
- create_daily_note  
- create_meeting_note  
- create_idea_note  
- create_todo_list  
- create_journal_entry  
- create_quick_note  
- create_goal_note  
- create_reminder_note  
- create_task_list  

---

🧠 Output Format:

✅ If matched:
```json
{
  "cluster": "note_ops",
  "intent": "<matched_intent_name>",
  "user_input": "<original_user_input>"
}

'''

    # Append user input to the content
    full_prompt = f"{system_prompt}\n\nuser_input: {user_msg}\nRespond with the correct JSON:"

    client = genai.Client(api_key="AIzaSyDXR4RwrPwanJbQjbnXyT-GYGPAmSYNBOg")
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=full_prompt
    )


    response_text = clean_response(response.text)
    save_json_safely(response_text)
