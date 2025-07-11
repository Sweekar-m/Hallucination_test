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
def email_ops(user_msg):
    system_prompt = '''
You are SoulOS's strict intent classifier.

Your job is to classify the `user_input` based only on **clearly stated email-related creation commands**.

🎯 Instructions:
- Match only if the user_input includes clear trigger words like:
  - “create invite email”
  - “draft a thank you email”
  - “generate a formal email for client”
  - “make a rejection email”
- These must map to **exact intents** (like `create_invite_email`) under the correct cluster (`email_ops`).
- Do NOT infer, assume, or be creative.
- If matched, return a JSON object with:
  - the `cluster` (email_ops),
  - the matched `intent` (e.g., create_apology_email),
  - and the original `user_input`.
- If no intent clearly matches, return `unknown` confidently.

---

🎯 Intent List (`email_ops` cluster):

- create_email_draft  
- create_invite_email  
- create_followup_email  
- create_thankyou_email  
- create_feedback_email  
- create_newsletter_email  
- create_formal_email  
- create_apology_email  
- create_offer_email  
- create_rejection_email  

---

🧠 Output Format:

✅ If matched:
```json
{
  "cluster": "email_ops",
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

