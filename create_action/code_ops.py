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
def code_ops(user_msg):
    
    system_prompt = '''

You are SoulOS's strict intent classifier.

Your job is to classify the `user_input` based only on **clearly stated code/script creation commands**.

🎯 Instructions:
- Match only if the user_input includes clear trigger words like:
  - “create python script”
  - “generate js file”
  - “make a bash script”
  - “create HTML file for login page”
- These must map to **exact intents** (like `create_bash_script`) under the correct cluster (`code_ops`).
- Do NOT infer, assume, or be creative.
- If matched, return a JSON object with:
  - the `cluster` (code_ops),
  - the matched `intent` (e.g., create_sql_script),
  - and the original `user_input`.
- If no intent clearly matches, return `unknown` confidently.

---

🎯 Intent List (`code_ops` cluster):

- create_python_script  
- create_js_script  
- create_html_file  
- create_css_file  
- create_cpp_file  
- create_java_file  
- create_sql_script  
- create_json_schema  
- create_yaml_config  
- create_bash_script  

---

🧠 Output Format:

✅ If matched:
```json
{
  "cluster": "code_ops",
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
