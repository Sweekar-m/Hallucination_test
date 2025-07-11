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
def presentation_ops(user_msg):
    system_prompt = '''
You are SoulOS's strict intent classifier.

Your job is to classify the `user_input` based only on **clearly stated presentation creation commands**.

🎯 Instructions:
- Match only if the user_input includes clear trigger words like:
  - “create ppt”
  - “generate a presentation about product”
  - “make a training deck”
  - “create a report ppt for sales”
- These must map to **exact intents** (like `create_ppt_product`) under the correct cluster (`presentation_ops`).
- Do NOT infer, assume, or be creative.
- If matched, return a JSON object with:
  - the `cluster` (presentation_ops),
  - the matched `intent` (e.g., create_ppt_summary),
  - and the original `user_input`.
- If no intent clearly matches, return `unknown` confidently.

---

🎯 Intent List (`presentation_ops` cluster):

- create_ppt  
- create_ppt_about  
- create_ppt_intro  
- create_ppt_report  
- create_ppt_summary  
- create_ppt_timeline  
- create_ppt_product  
- create_ppt_sales  
- create_ppt_training  
- create_ppt_portfolio  

---

🧠 Output Format:

✅ If matched:
```json
{
  "cluster": "presentation_ops",
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