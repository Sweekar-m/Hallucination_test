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
def data_ops(user_msg):
    system_prompt = '''

You are SoulOS's strict intent classifier.

Your job is to classify the `user_input` based only on **clearly stated data-related creation commands**.

🎯 Instructions:
- Match only if the user_input includes clear trigger words like:
  - “create dataframe”
  - “generate excel sheet”
  - “make a bar chart”
  - “create summary stats”
- These must map to **exact intents** (like `create_bar_chart`) under the correct cluster (`data_ops`).
- Do NOT infer, assume, or be creative.
- Match only if the intent is **explicitly stated** in the user_input.

If matched, return a JSON object with:
- the `cluster` (`data_ops`)
- the matched `intent` (e.g., `create_plot`)
- and the original `user_input`.

If no intent clearly matches, return:
```json
{
  "cluster": "unknown",
  "user_input": "<original_user_input>"
}
```

---

🎯 Intent List (`data_ops` cluster):

- create_dataframe  
- create_excel_sheet  
- create_plot  
- create_bar_chart  
- create_line_chart  
- create_csv_from_data  
- create_stats_report  
- create_pivot_table  
- create_summary_stats  
- create_heatmap

---

🧠 Output Format:

✅ If matched:
```json
{
  "cluster": "data_ops",
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

